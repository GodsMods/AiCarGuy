import streamlit as st
import time
import openai
from duckduckgo_search import DDGS

############################
# 1. OpenAI client with new usage
############################
# We'll create an openai.Client with your API key from secrets:
client = openai.Client(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AiCarGuy – GPT-3.5 with Conversation Memory", layout="wide")

AUTOMOTIVE_KEYWORDS = [
    # General
    "car", "vehicle", "automotive", "repair", "maintenance", "upgrade", "mod",
    "aftermarket", "performance", "tuning", "diagnostic",

    # Engine & Drivetrain
    "engine", "motor", "head gasket", "valve cover", "crankshaft", "camshaft",
    "piston", "cylinder", "spark plug", "ignition coil", "distributor", "fuel pump",
    "fuel injector", "carburetor", "oil filter", "oil pan", "oil leak", "oil change",
    "oil cooler", "oil pressure", "oil level", "dipstick", "radiator", "coolant",
    "thermostat", "water pump", "belt", "timing belt", "timing chain", "chain tensioner",
    "serpentine belt", "idler pulley", "belt tensioner", "engine mount", "valve train",
    "valve lash", "lifters", "pushrods", "head bolts", "cam phaser", "vvt solenoid",
    "pcv valve", "breather", "crankcase", "fuel tank", "fuel line", "fuel pressure",
    "fuel rail", "injector cleaning", "intake manifold", "exhaust manifold", "headers",
    "downpipe", "turbo", "supercharger", "forced induction", "wastegate", "blow-off valve",
    "intercooler", "boost controller", "boost gauge", "boost leak", "turbine", "compressor",
    "throttle body", "maf sensor", "map sensor", "o2 sensor", "knock sensor", "engine swap",
    "ls swap", "transmission", "gearbox", "clutch", "flywheel", "pressure plate", "throwout bearing",
    "pilot bearing", "torque converter", "synchro", "gear slip", "valve body", "shift solenoid",
    "trans fluid", "trans cooler", "overdrive", "transfer case", "axle", "differential",
    "gear ratio", "limited slip diff", "cv axle", "cv joint", "u-joint", "driveshaft",

    # Cooling & Heating
    "cooling system", "radiator cap", "heater core", "fan clutch", "electric fan",
    "coolant flush", "overheating", "ac compressor", "condenser", "evaporator", "hvac",
    "blower motor", "ac recharge", "ac leak", "heater not working",

    # Ignition & Electrical
    "battery", "alternator", "starter", "spark plug wire", "distributor cap", "rotor",
    "coil pack", "fuse box", "relay", "wiring harness", "ground wire", "check engine light",
    "obd", "obd-ii", "trouble code", "scan tool", "security light", "car alarm", "key fob",
    "remote start", "immobilizer", "pcm", "ecu", "remap", "chip tuning",

    # Fuel & Air
    "carburetor tuning", "air filter", "cold air intake", "intake piping", "fuel pump relay",
    "fuel gauge", "fuel trim", "runs rich", "runs lean", "vacuum leak", "evap system",

    # Exhaust & Emissions
    "exhaust", "muffler", "resonator", "cat-back", "catalytic converter", "p0420",
    "emissions test", "lambda sensor", "dpf", "egr valve", "def fluid", "scr",

    # Brakes & Suspension
    "brake", "rotor", "caliper", "brake pad", "drum brake", "master cylinder", "abs",
    "brake fluid", "brake line", "vacuum brake booster", "shock absorber", "strut",
    "coil spring", "leaf spring", "control arm", "ball joint", "tie rod", "alignment",
    "camber", "caster", "toe", "coilover", "lift kit", "lowering springs",

    # Wheels & Tires
    "tire", "lugnut", "wheel nut", "wheel bearing", "hub assembly", "tpms", "wheel alignment",
    "spacers", "rim", "offset",

    # Steering
    "steering rack", "rack and pinion", "steering column", "power steering pump", "power steering fluid",
    "pitman arm", "idler arm",

    # Drivetrain Configurations
    "4wd", "awd", "fwd", "rwd", "transfer case fluid", "locking hub",

    # Body & Exterior
    "rust repair", "fender", "bumper", "hood", "tailgate", "door panel", "paint correction",
    "ceramic coating", "body filler", "chassis", "frame", "bed liner",

    # Interior & HVAC
    "dashboard", "instrument cluster", "heater core", "hvac blend door", "blower resistor",
    "ac vent", "car detailing",

    # Diagnostics & Codes
    "p0171", "p0300", "p0455", "p0128", "check engine light", "misfire", "rough idle",
    "stalling", "obd code", "trouble code",

    # Fluids & Filters
    "engine oil", "transmission fluid", "differential fluid", "gear oil", "brake fluid",
    "power steering fluid", "coolant flush", "fuel filter", "air filter", "cabin air filter",

    # Common Symptoms
    "car wont start", "engine stall", "overheating", "smoke from exhaust", "oil leak",
    "coolant leak", "trans leak", "brake squeal", "steering vibration", "pulls to one side",
    "clunk noise", "grinding noise", "whining noise", "belt squeak", "engine knock",

    # Upgrades & Mods
    "intake manifold upgrade", "exhaust manifold upgrade", "turbo kit", "supercharger kit",
    "intercooler upgrade", "downpipe upgrade", "fuel system upgrade", "injector upgrade",
    "engine swap", "ls swap", "headers", "catback exhaust", "coilovers", "big brake kit",
    "tuner", "ecu remap", "flash tune", "nitrous oxide", "nos", "turbo spool", "wastegate",
    "boost controller", "e85 conversion",

    # Specific Vehicles & Brands
    "gmc sierra", "chevy silverado", "ford f-150", "toyota tacoma", "honda civic", "subaru wrx",
    "dodge ram", "jeep wrangler", "nissan altima", "mazda miata", "bmw m3", "mercedes c-class",
    "audi a4", "volkswagen gti", "hyundai sonata", "kia optima",

    # Additional Terms
    "car battery", "car alarm", "immobilizer", "security system", "obd code reader",
    "car shakes when braking", "car wont accelerate", "trans slip", "clutch slip",
    "turbo spool sound", "knock sensor", "mass air flow sensor", "intake leak",
    "catalytic converter code", "dpfe sensor", "fuel pressure regulator",
    "diesel glow plug", "diesel particulate filter", "transfer case motor",
    "4x4 actuator", "wheel speed sensor", "abs module", "cam sensor", "crank sensor",
    "pcv valve", "breather hose", "car stalling at idle", "engine vacuum",
    "engine mount replacement", "steering rack replacement", "transmission cooler lines",
    "cv axle replacement", "driveshaft u-joint"
]

def is_automotive_query(query):
    return any(k in query.lower() for k in AUTOMOTIVE_KEYWORDS)

############################
# 2. DuckDuckGo domain-limited search
############################
def domain_search_godsmods(query):
    query = query.strip()
    if not query:
        return "No product link found (empty query)."
    time.sleep(1)  # small delay to avoid rate-limiting

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(f"site:godsmods.shop {query}", max_results=3))
    except Exception as e:
        return f"Error searching godsmods.shop: {str(e)}"

    if not results:
        return "No product link found for that query on godsmods.shop."

    link_info = ""
    for r in results:
        title = r.get("title", "")
        body = r.get("body", "")
        link_info += f"{title}: {body}\n"

    return link_info.strip() if link_info else "No direct product link found."

############################
# 3. DuckDuckGo general snippet
############################
def general_web_snippet(query):
    query = query.strip()
    if not query:
        return "No general automotive info found (empty query)."
    time.sleep(1)

    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query + " automotive repair", max_results=3))
    except Exception as e:
        return f"Error searching general automotive info: {str(e)}"

    if not results:
        return "No general automotive info found."

    snippet = ""
    for r in results:
        snippet += f"{r.get('title','')}: {r.get('body','')}\n"
    return snippet.strip()

############################
# 4. GPT-3.5 call with conversation memory
############################
def call_gpt35(messages):
    """
    messages: list of {role: user/assistant/system, content: str}
    using the new openai.Client chat.completions.create
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content

############################
# 5. Build final answer (with memory)
############################
def answer_query(user_query):
    # If user query is not automotive, short-circuit
    if not is_automotive_query(user_query):
        return "I only answer automotive repair or upgrade questions. Please ask something car-related."

    # domain-limited search for product link
    product_links = domain_search_godsmods(user_query)
    # general snippet
    web_info = general_web_snippet(user_query)

    # We'll insert the new context as an assistant message
    # so the model sees it in the conversation
    context_message = {
        "role": "assistant",
        "content": (
            f"Here is some product info from godsmods.shop:\n{product_links}\n\n"
            f"Here is some general automotive web info:\n{web_info}"
        )
    }

    # Insert system instructions if this is the first user query
    # or if you prefer to always keep them at the start of the conversation
    messages = []
    found_system = any(m["role"] == "system" for m in st.session_state["messages"])
    if not found_system:
        messages.append({"role": "system", "content": "You are a helpful automotive repair and upgrade expert. You ONLY answer automotive questions, general greetings, and product_based search queries."})

    # Add all prior conversation from st.session_state
    messages.extend(st.session_state["messages"])

    # Add the new context as an assistant message
    messages.append(context_message)
    # Then add the user's new question
    messages.append({"role": "user", "content": user_query})

    # Call GPT
    final_answer = call_gpt35(messages)

    # Return final answer
    return final_answer

############################
# 6. Streamlit UI
############################
st.title("🚗 AiCarGuy")

# session_state["messages"] holds the entire conversation
if "messages" not in st.session_state:
    # Initialize with an empty list
    st.session_state["messages"] = []

user_input = st.text_input("Ask an automotive or product-based question:")

if st.button("Submit"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        reply = answer_query(user_input)
        # Add the user's question and the assistant's reply to session memory
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.session_state["messages"].append({"role": "assistant", "content": reply})

for msg in reversed(st.session_state["messages"]):
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**AiCarGuy:** {msg['content']}")
    st.write("---")
