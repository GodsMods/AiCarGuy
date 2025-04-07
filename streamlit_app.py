import streamlit as st
import time
import openai
from duckduckgo_search import DDGS

############################
# 1. OpenAI client with new usage
############################
client = openai.Client(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AiCarGuy", layout="wide")

# Comprehensive list of automotive keywords (highly extensive)
AUTOMOTIVE_KEYWORDS = [
    "car", "vehicle", "automotive", "repair", "maintenance", "upgrade", "mod",
    "aftermarket", "performance", "tuning", "diagnostic", "engine", "motor",
    "head gasket", "valve cover", "crankshaft", "camshaft", "piston", "cylinder",
    "spark plug", "ignition coil", "distributor", "fuel pump", "fuel injector",
    "carburetor", "oil filter", "oil pan", "oil leak", "oil change", "oil cooler",
    "oil pressure", "oil level", "dipstick", "radiator", "coolant", "thermostat",
    "water pump", "belt", "timing belt", "timing chain", "chain tensioner",
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
    "cooling system", "radiator cap", "heater core", "fan clutch", "electric fan",
    "coolant flush", "overheating", "ac compressor", "condenser", "evaporator", "hvac",
    "blower motor", "ac recharge", "ac leak", "heater not working", "battery", "alternator",
    "starter", "spark plug wire", "distributor cap", "rotor", "coil pack", "fuse box", "relay",
    "wiring harness", "ground wire", "check engine light", "obd", "obd-ii", "trouble code",
    "scan tool", "security light", "car alarm", "key fob", "remote start", "immobilizer", "pcm",
    "ecu", "remap", "chip tuning", "obd2", "fuse block", "carburetor tuning", "air filter",
    "cold air intake", "intake piping", "fuel pump relay", "fuel gauge", "fuel trim", "runs rich",
    "runs lean", "vacuum leak", "evap system", "exhaust", "muffler", "resonator", "cat-back",
    "catalytic converter", "p0420", "emissions test", "lambda sensor", "dpf", "egr valve",
    "def fluid", "scr", "brake", "rotor", "caliper", "brake pad", "drum brake", "master cylinder",
    "abs", "brake fluid", "brake line", "vacuum brake booster", "shock absorber", "strut",
    "coil spring", "leaf spring", "control arm", "ball joint", "tie rod", "alignment", "camber",
    "caster", "toe", "coilover", "lift kit", "lowering springs", "tire", "lugnut", "wheel nut",
    "wheel bearing", "hub assembly", "tpms", "wheel alignment", "spacers", "rim", "offset",
    "steering rack", "rack and pinion", "steering column", "power steering pump", "power steering fluid",
    "pitman arm", "idler arm", "4wd", "awd", "fwd", "rwd", "transfer case fluid", "locking hub",
    "4 wheel drive", "all wheel drive", "rust repair", "fender", "bumper", "hood", "tailgate",
    "door panel", "paint correction", "ceramic coating", "body filler", "chassis", "frame",
    "bed liner", "bondo", "dashboard", "instrument cluster", "heater core", "hvac blend door",
    "blower resistor", "ac vent", "car detailing", "air", "ac", "heat", "p0171", "p0300", "p0455",
    "p0128", "misfire", "rough idle", "stalling", "engine oil", "transmission fluid", "differential fluid",
    "gear oil", "power steering fluid", "coolant flush", "fuel filter", "cabin air filter", "car wont start",
    "engine stall", "smoke from exhaust", "coolant leak", "trans leak", "brake squeal", "steering vibration",
    "pulls to one side", "clunk noise", "grinding noise", "whining noise", "belt squeak", "engine knock",
    "intake manifold upgrade", "exhaust manifold upgrade", "turbo kit", "supercharger kit", "intercooler upgrade",
    "downpipe upgrade", "fuel system upgrade", "injector upgrade", "catback exhaust", "coilovers", "big brake kit",
    "tuner", "ecu remap", "flash tune", "nitrous oxide", "nos", "turbo spool", "e85 conversion",
    "gmc sierra", "chevy silverado", "ford f-150", "toyota tacoma", "honda civic", "subaru wrx",
    "dodge ram", "jeep wrangler", "nissan altima", "mazda miata", "bmw m3", "mercedes c-class",
    "audi a4", "volkswagen gti", "hyundai sonata", "kia optima", "nissan titan", "car battery",
    "car shakes when braking", "car wont accelerate", "trans slip", "clutch slip", "mass air flow sensor",
    "intake leak", "catalytic converter code", "dpfe sensor", "fuel pressure regulator", "diesel glow plug",
    "diesel particulate filter", "transfer case motor", "4x4 actuator", "wheel speed sensor", "abs module",
    "cam sensor", "crank sensor", "car stalling at idle", "engine vacuum", "engine mount replacement",
    "steering rack replacement", "transmission cooler lines", "cv axle replacement", "driveshaft u-joint"
    # ... (add more terms as needed for ultra-specific repair queries)
]

def is_automotive_query(query):
    return any(k in query.lower() for k in AUTOMOTIVE_KEYWORDS)

############################
# 2. DuckDuckGo domain-limited search for godsmods.shop
############################
def domain_search_godsmods(query):
    query = query.strip()
    if not query:
        return "No product link found (empty query)."
    time.sleep(1)  # delay to avoid rate-limiting

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
# 3. DuckDuckGo general automotive info search
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
# 4. GPT-4o mini call with conversation memory (new OpenAI client usage)
############################
def call_gpt35(messages):
    response = client.chat.completions.create(
        model="gpt-4o-mini-2024-07-18",
        messages=messages,
        temperature=0.7
    )
    return response.choices[0].message.content

############################
# 5. Build final answer (with memory)
############################
def answer_query(user_query):
    if not is_automotive_query(user_query):
        return "I only answer automotive repair or upgrade questions. Please ask something car-related."

    product_links = domain_search_godsmods(user_query)
    web_info = general_web_snippet(user_query)

    context_message = {
        "role": "assistant",
        "content": (
            f"Here is some product info from godsmods.shop:\n{product_links}\n\n"
            f"Here is some general automotive web info:\n{web_info}"
        )
    }

    messages = []
    # Insert system instruction only once
    if not any(m["role"] == "system" for m in st.session_state["messages"]):
        messages.append({"role": "system", "content": "You are a helpful automotive repair and upgrade expert. You ONLY answer automotive questions."})
    
    # Add prior conversation from session state
    messages.extend(st.session_state["messages"])
    messages.append(context_message)
    messages.append({"role": "user", "content": user_query})

    final_answer = call_gpt35(messages)
    return final_answer

############################
# 6. Streamlit UI with persistent conversation history
############################
st.title("🚗 AiCarGuy")

# Initialize conversation history if not present
if "messages" not in st.session_state:
    st.session_state["messages"] = []

user_input = st.text_input("Ask an automotive or product-based question:")

if st.button("Submit"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        reply = answer_query(user_input)
        # Save the latest exchange to conversation history
        st.session_state["messages"].append({"role": "user", "content": user_input})
        st.session_state["messages"].append({"role": "assistant", "content": reply})

# Display conversation history (most recent first)
for msg in reversed(st.session_state["messages"]):
    if msg["role"] == "user":
        st.markdown(f"**You:** {msg['content']}")
    elif msg["role"] == "assistant":
        st.markdown(f"**AiCarGuy:** {msg['content']}")
    st.write("---")
