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
    # Original List Terms (Maintained)
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
    "steering rack replacement", "transmission cooler lines", "cv axle replacement", "driveshaft u-joint",

    # Expanded Technical Terms
    "VVT-i", "DOHC", "SOHC", "VTEC", "MIVEC", "SkyActiv", "EcoBoost", "HEMI", "Rotary 13B",
    "boxer engine", "common rail diesel", "piezo injectors", "dual mass flywheel", "quattro system",
    "xDrive", "SH-AWD", "4Matic", "torque vectoring", "torsen differential", "haldex clutch",
    "locking differential", "posi traction", "limited slip", "direct injection", "port injection",
    "twin-scroll turbo", "variable geometry turbo", "anti-lag system", "launch control",
    "flat-plane crank", "cross-plane crank", "forged internals", "billet aluminum", "CNC porting",
    "deck plating", "zero deck clearance", "piston slap", "rod knock", "main bearing clearance",
    "thrust bearing", "windage tray", "crank scraper", "oil galley", "coolant crossover", "frost plug",
    "core plug", "head studs", "ARP bolts", "MLS gasket", "cometic gasket", "O-ringed block",
    "dry sump", "wet sump", "crankcase ventilation", "catch can", "AOS", "PCV system", "EGR delete",
    "DPF delete", "SCR delete", "tuner software", "bench flash", "bootmod", "cobb accessport",
    "piggyback ECU", "standalone ECU", "Megasquirt", "AEM EMS", "Haltech", "MoTeC", "HP Tuners",
    "Ethanol content sensor", "flex fuel", "meth injection", "water/meth", "progressive controller",
    "boost by gear", "launch control", "2-step rev limiter", "rolling anti-lag", "burble tune",
    "crackle map", "popcorn tune", "catless downpipe", "test pipe", "resonator delete", "X-pipe",
    "H-pipe", "true dual exhaust", "axle-back", "turbo-back", "header wrap", "heat blanket",
    "thermal coating", "ceramic coating", "sway bar", "anti-roll bar", "strut tower brace",
    "chassis bracing", "subframe connectors", "polyurethane bushings", "spherical bearings",
    "adjustable control arms", "camber plates", "toe arms", "traction bars", "panhard rod",
    "Watt's linkage", "multi-link suspension", "double wishbone", "MacPherson strut",
    "semi-trailing arm", "torque arm", "Chapman strut", "De Dion tube", "uni-body construction",
    "body-on-frame", "hydroforming", "crumple zones", "side impact beams", "crumple zones",
    "collision repair", "frame straightening", "pull chain", "measuring system", "John Beam",
    "Celette bench", "structural adhesive", "spot welds", "plug welds", "MIG welding",
    "TIG welding", "plasma cutter", "body hammers", "dolly blocks", "shrinking disc",
    "metal finishing", "lead loading", "rust converter", "POR-15", "undercoating",
    "cavity wax", "electronic rust prevention", "galvanic corrosion", "dissimilar metals",
    "electrolysis corrosion", "stone chips", "clear coat failure", "orange peel",
    "buffer trails", "DA polisher", "rotary polisher", "cutting compound", "polishing compound",
    "ceramic coating", "graphene coating", "PPF", "paint protection film", "vinyl wrap",
    "color change wrap", "matte finish", "chrome delete", "blackout package", "murdered out",
    "stance", "hellaflush", "poke", "stretch tires", "negative camber", "drifting",
    "time attack", "autocross", "rallycross", "drag racing", "road racing", "circle track",
    "off-road", "rock crawling", "overlanding", "prerunner", "Baja", "trophy truck",
    "tube chassis", "roll cage", "NASA certification", "FIA homologation", "NHRA certification",
    "SFI rating", "fire suppression", "kill switch", "battery disconnect", "fuel cell",
    "racing harness", "HANS device", "data logger", "OBD2 logger", "dashdaq", "racepak",
    "AIM system", "ECU telemetry", "CAN bus", "LIN bus", "MOST bus", "FlexRay", "OBD-II PID",
    "parameter IDs", "live data", "freeze frame", "pending codes", "permanent codes",
    "manufacturer specific codes", "enhanced diagnostics", "bi-directional control",
    "component testing", "actuator test", "output test", "adaptation values", "long term fuel trim",
    "short term fuel trim", "fuel system status", "calculated load", "engine load",
    "ignition advance", "injector pulse width", "duty cycle", "MAF rate", "MAP value",
    "evap purge", "purge flow", "tank pressure", "EGR flow", "commanded AFR", "wideband O2",
    "narrowband O2", "lambda value", "equivalence ratio", "knock count", "knock retard",
    "VVT position", "camshaft offset", "crankshaft variation", "misfire counter",
    "cylinder contribution", "relative compression", "cylinder leakage", "running compression",
    "dynamic compression", "static compression", "quench height", "squish velocity",
    "piston speed", "rod ratio", "dwell time", "spark duration", "ion sensing",
    "combustion analysis", "pre-ignition", "detonation", "LSPI", "low speed pre-ignition",
    "carbon buildup", "walnut blasting", "media blasting", "chemical cleaning",
    "induction service", "top engine cleaner", "seafoam", "decarbonization",
    "oil consumption", "blue smoke", "white smoke", "black smoke", "fuel dilution",
    "glycol contamination", "TSB lookup", "recall lookup", "service campaign",
    "wiring diagram", "component locator", "labor time", "flat rate", "book time",
    "warranty time", "diag time", "customer pay", "warranty repair", "goodwill repair",
    "aftermarket warranty", "extended warranty", "factory warranty", "powertrain warranty",
    "bumper-to-bumper", "certified pre-owned", "lemon law", "diminished value",
    "total loss", "salvage title", "rebuilt title", "branded title", "odometer fraud",
    "VIN cloning", "title washing", "vehicle history", "Carfax", "AutoCheck",
    "NMVTIS", "title search", "registration check", "license plate lookup",

    # Common Misspellings & Alternate Phrasings
    "break pads", "breaks", "roter", "calilper", "exhuast", "catylitic converter",
    "oxyegen sensor", "distributer", "alternater", "serpantine belt", "timming chain",
    "cam position senser", "crank posision sensor", "mass airflow", "map senser",
    "throtle body", "intercooler", "turbocharger", "supercharger", "nos system",
    "e85 fuel", "chip tuning", "ecu flash", "tunning", "allignment", "camber adjustment",
    "tire rotation", "oil chnage", "coolent flush", "transmission fliud", "diff fluid",
    "power steering leak", "axle seal", "valve cover gasket", "head gasket replacement",
    "spark plug gap", "ignition timing", "fuel filter replacement", "air filter change",
    "cabin filter replacement", "timing belt service", "water pump replacement",
    "thermostat replacement", "radiator replacement", "ac recharge", "ac compressor replacement",
    "battery replacement", "alternator replacement", "starter replacement", "fuel pump replacement",
    "ignition coil replacement", "oxygen sensor replacement", "catalytic converter replacement",
    "muffler replacement", "struts replacement", "shocks replacement", "brake job",
    "rotor resurfacing", "caliper rebuild", "wheel bearing replacement", "tie rod replacement",
    "ball joint replacement", "control arm replacement", "sway bar link replacement",
    "cv axle replacement", "wheel alignment cost", "transmission rebuild cost",
    "engine rebuild cost", "head gasket repair cost", "turbo replacement cost",
    "car won't start", "car not starting", "clicking noise when starting",
    "slow cranking", "no crank", "engine turns over but won't start", "check engine light on",
    "check engine light flashing", "car shaking", "vibration at highway speeds",
    "steering wheel shake", "brake pedal pulsation", "grinding noise when braking",
    "squealing noise when braking", "clunking noise over bumps", "whining noise from transmission",
    "howling noise from differential", "hissing noise from engine", "ticking noise from engine",
    "knocking noise from engine", "smell of gas in cabin", "burning oil smell",
    "sweet smell from vents", "steam from engine bay", "fluid under car",
    "red fluid leak", "green fluid leak", "brown fluid leak", "clear fluid leak",
    "car overheating", "temperature gauge high", "heater blowing cold air",
    "ac not cold", "weak airflow from vents", "window won't roll up",
    "door lock not working", "key stuck in ignition", "radio not working",
    "bluetooth not connecting", "backup camera not working", "navigation system update",
    "tire pressure warning light", "abs light on", "traction control light on",
    "airbag light on", "battery light on", "oil light on", "coolant light on",
    "4wd light flashing", "service engine soon", "service transmission",
    "service stability system", "limp mode", "reduced power mode",

    # Regional/Localized Terms
    "mot test", "tüv inspection", "wof check", "roadworthy certificate",
    "pink slip", "green slip", "rego check", "road tax", "vehicle excise duty",
    "congestion charge", "ULEZ compliance", "ZEV mandate", "CA smog check",
    "BAR referee", "inspections sticker", "safety inspection", "emissions test",
    "dyno test", "rolling road", "tune shop", "speed shop", "jdm parts",
    "euro parts", "domestic parts", "gray market", "parallel import",
    "homologation special", "type approval", "ADR compliance", "DOT approval",
    "SAE standards", "ISO certification", "OEM specifications", "aftermarket parts",
    "remanufactured parts", "rebuilt parts", "used parts", "junkyard parts",
    "pick-n-pull", "auto recycler", "breaker yard", "salvage yard",

    # Ultra-Specific Technical Terms
    "hall effect sensor", "reluctor wheel", "tone ring gap", "variable reluctance sensor",
    "piezoelectric knock sensor", "thermistor coolant sensor", "stepper motor IAC valve",
    "pulse width modulated fan", "LIN-controlled headlight", "CAN bus gateway module",
    "most fiber optic ring", "telematic control unit", "body domain controller",
    "zone controller", "smart junction box", "high speed CAN", "low speed CAN",
    "flexray network", "ethernet in automotive", "automotive cybersecurity",
    "OTA updates", "vehicle-to-cloud", "V2X communication", "tire pressure sensor ID",
    "TPMS relearn procedure", "membrane switch panel", "haptic feedback controls",
    "capacitive touch", "resistive touch", "head-up display calibration",
    "night vision calibration", "lidar sensor", "radar sensor", "camera calibration",
    "ADAS calibration", "dynamic calibration", "static calibration", "target alignment",
    "wheel speed sensor air gap", "active wheel speed sensor", "passive wheel speed sensor",
    "magnetoresistive sensor", "giant magnetoresistance", "reed switch", "wiegand sensor",
    "inductive sensor", "optical sensor", "phototransistor", "infrared sensor",
    "ultrasonic sensor", "parking sensor", "blind spot radar", "lane keep assist camera",
    "rain/light sensor", "humidity sensor", "solar load sensor", "seat occupancy sensor",
    "weight classification", "pyrotechnic pretensioner", "squib circuit", "clock spring",
    "rollover sensor", "yaw rate sensor", "lateral accelerometer", "longitudinal accelerometer",
    "vertical accelerometer", "gyroscope", "inclinometer", "steering angle sensor initialization",
    "zero point calibration", "torque sensor", "electric power steering motor",
    "brushless DC motor", "motor position sensor", "resolver", "encoder", "hall effect sequence",
    "PWM control", "current monitoring", "motor phase", "inverter module", "IGBT transistor",
    "gate driver", "DC-DC converter", "voltage regulator", "load response control",
    "energy management", "start-stop battery", "AGM battery", "EFB battery", "SOC calculation",
    "SOH estimation", "cell balancing", "battery thermal management", "preheating circuit",
    "regenerative braking", "blended braking", "friction braking", "brake blending",
    "hill hold", "auto hold", "electronic parking brake", "EPB calibration", "brake pad wear sensor",
    "wireless charging", "conductive charging", "CCS connector", "CHAdeMO", "Type 2 connector",
    "SAE J1772", "ISO 15118", "PLC communication", "charging curve", "C-rate", "thermal derating",
    "preconditioning", "battery cooling", "chiller circuit", "PTC heater", "heat pump",
    "refrigerant type", "R1234yf", "CO2 refrigerant", "compressor oil", "desiccant bag",
    "receiver dryer", "expansion valve", "orifice tube", "suction line", "discharge line",
    "liquid line", "evaporator freeze protection", "high pressure cutout", "low pressure cutout",
    "pressure transducer", "manifold gauge", "sniffer probe", "dye injection", "UV leak detection",
    "electronic leak detector", "vacuum decay test", "nitrogen pressure test", "bubble test",
    "schrader valve", "service port", "quick connect", "snap lock", "o-ring seal",
    "gasket sealant", "RTV silicone", "anaerobic sealant", "thread locker", "anti-seize",
    "torque specs", "torque sequence", "angle torque", "yield torque", "prevailing torque",
    "torque-to-yield", "stretch bolts", "plastic deformation", "elastic deformation",
    "fatigue failure", "shear stress", "tensile strength", "Rockwell hardness", "Brinell hardness",
    "surface finish", "Ra value", "honed surface", "crosshatch pattern", "glaze breaker",
    "cylinder deglazing", "ridge reamer", "ball hone", "flex hone", "diamond stone",
    "surface plate", "straight edge", "feeler gauge", "micrometer", "telescoping gauge",
    "bore gauge", "dial indicator", "plastigage", "thread pitch gauge", "digital angle gauge",
    "laser thermometer", "thermal camera", "stethoscope", "vacuum gauge", "fuel pressure tester",
    "compression tester", "leak-down tester", "smoke machine", "voltmeter", "amp clamp",
    "oscilloscope", "lab scope", "graphing multimeter", "power probe", "noid light",
    "test light", "logical probe", "breakout box", "pinout diagram", "terminal repair",
    "weatherpack connector", "metri-pack connector", "deutsch connector", "molex connector",
    "crimp tool", "wire gauge", "stranded vs solid", "tin-plated copper", "CSA rating",
    "voltage drop", "parasitic drain", "dark current", "sleep mode", "wake-up signal",
    "bus wake-up", "LIN wake-up", "CAN wake-up", "network topology", "star configuration",
    "daisy chain", "termination resistor", "bus load", "message priority", "arbitration",
    "error frame", "bus off", "error passive", "error active", "UDS protocol", "KWP2000",
    "ISO-TP", "CAN FD", "J1939", "J1979", "J2534", "RP1210", "DoIP", "XCP protocol",
    "CCP protocol", "bootloader", "reflash", "reprogram", "software update", "VIN programming",
    "immobilizer sync", "key learning", "transponder chip", "RFID", "NFC", "BLE pairing",
    "telematics unit", "eCall", "bCall", "connected car", "vehicle tracking", "geofencing",
    "driver behavior monitoring", "usage-based insurance", "predictive maintenance",
    "condition-based monitoring", "remaining useful life", "failure prediction",
    "neural network", "machine learning", "AI diagnostics", "pattern recognition",
    "predictive analytics", "digital twin", "virtual sensor", "sensor fusion",
    "kalman filter", "data smoothing", "time series analysis", "Fourier transform",
    "frequency domain", "time domain", "waveform analysis", "capture buffer",
    "math channel", "PID streaming", "histogram view", "parameter graphing",
    "flight recorder", "black box", "event logger", "freeze frame data",
    "snapshot data", "data mining", "big data analytics", "cloud diagnostics",
    "remote diagnostics", "over-the-air updates", "telematics interface",
    "shop management system", "DMS integration", "shop workflow", "service writer",
    "tech line support", "hotline assistance", "technical bulletins", "TSB lookup",
    "wiring diagram access", "component locator", "labor time guide", "parts cross-reference",
    "OEM part numbers", "aftermarket equivalents", "competitor part numbers",
    "supplier cross", "interchange information", "supersession history",
    "part number cleanup", "VIN-specific parts", "build sheet", "option codes",
    "trim level", "package codes", "production date", "manufacturing plant",
    "country of origin", "import codes", "homologation version", "market variant",
    "country-specific tuning", "emissions package", "calibration part number",
    "software version", "ECU hardware number", "TCU software level", "ASAM ODX",
    "MDF-4 format", "diagnostic trouble code", "DTC severity", "DTC priority",
    "DTC aging counter", "DTC freeze frame", "DTC snapshot", "DTC status",
    "pending DTC", "confirmed DTC", "permanent DTC", "emissions-related DTC",
    "non-emissions DTC", "manufacturer-specific DTC", "SAE-defined DTC",
    "network DTC", "U-code", "B-code", "C-code", "Uxxxx", "Bxxxx", "Cxxxx",
    "P-code", "Pxxxx", "powertrain DTC", "chassis DTC", "body DTC", "network DTC",
    "subsystem DTC", "component DTC", "rationality check", "component protection",
    "component initialization", "parameterization", "coding", "adaptation",
    "basic settings", "output tests", "actuator tests", "input tests",
    "sensor validation", "signal plausibility", "component protection",
    "secure gateway", "authentication", "challenge-response", "seed-key",
    "PIN code", "security access", "factory tool", "dealer-level access",
    "independent shop access", "reverse engineering", "tuner-level access",
    "bench tuning", "on-car tuning", "live tuning", "speed density",
    "MAF-based tuning", "alpha-N tuning", "closed loop", "open loop",
    "fuel map", "ignition map", "boost map", "VVT map", "ethanol map",
    "temperature compensation", "barometric correction", "altitude compensation",
    "ego correction", "long term fuel trim", "short term fuel trim",
    "adaptive learning", "reset adaptations", "clear learned values",
    "write entire", "write calibration", "flash count", "CVN verification",
    "checksum correction", "tuner checksum", "ROM checksum", "signature",
    "anti-tune", "tuner detection", "TD1 flag", "warranty void",
    "tune detection", "flash counter", "security update", "countermeasure",
    "tuner-unlock", "boot mode", "recovery mode", "bricked ECU",
    "ECU recovery", "bench power supply", "BDM port", "JTAG interface",
    "hex editing", "disassembly", "reverse compile", "definition files",
    "XDF files", "A2L files", "Damos files", "map switching", "real-time tuning",
    "SD card tuning", "switchable maps", "valet mode", "kill mode",
    "anti-theft", "speed limiter", "rev limiter", "launch control",
    "flat foot shifting", "no-lift shift", "auto-blip", "throttle blip",
    "dec", 
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
