import streamlit as st
import time
import openai
from duckduckgo_search import DDGS

############################
# 1. Set up your OpenAI client
############################
# According to the new approach, we create an openai.Client with your API key:
client = openai.Client(api_key=st.secrets["OPENAI_API_KEY"])

st.set_page_config(page_title="AiCarGuy – GPT-3.5 + Domain Search", layout="wide")

AUTOMOTIVE_KEYWORDS = [
    "car","engine","brake","tire","vehicle","automotive","transmission",
    "exhaust","repair","maintenance","mod","lugnut","wheel","coolant","oil",
    "fluid","battery","spark plug","radiator","alternator","starter","ignition",
    "fuel","sensor","sierra","gmc","chevrolet","ford","honda","toyota"
]

def is_automotive_query(query):
    q_lower = query.lower()
    return any(k in q_lower for k in AUTOMOTIVE_KEYWORDS)

############################
# 2. The new Chat Completions API
############################
def call_gpt35(messages):
    """
    Uses the new openai.Client with the chat.completions.create method.
    messages: a list of dicts in the style of GPT-3.5 chat format
    """
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    # The returned object is an openai.types.Object object. Convert to dict or directly:
    # response.choices[0].message.content
    return response.choices[0].message.content

############################
# 3. Domain-limited search for godsmods.shop
############################
def domain_search_godsmods(query):
    """
    Searches only site:godsmods.shop for relevant product links or info.
    Returns a short snippet or error message if none found.
    """
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
# 4. General automotive snippet
############################
def general_web_snippet(query):
    """
    General automotive info search. Also uses a small delay & generic exception handling.
    """
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
# 5. Build final answer
############################
def answer_query(user_query):
    # 1) Domain check
    if not is_automotive_query(user_query):
        return "I only answer automotive repair or upgrade questions. Please ask something car-related."

    # 2) domain-limited search
    product_links = domain_search_godsmods(user_query)

    # 3) general snippet
    web_info = general_web_snippet(user_query)

    # 4) Build the messages
    messages = [
        {"role": "system", "content": "You are a helpful automotive repair and upgrade expert. You ONLY answer automotive questions."},
        {
            "role": "assistant",
            "content": (
                f"Here is some product info from godsmods.shop:\n{product_links}\n\n"
                f"Here is some general automotive web info:\n{web_info}"
            )
        },
        {"role": "user", "content": user_query}
    ]
    final_answer = call_gpt35(messages)
    return final_answer

############################
# 6. Streamlit UI
############################
st.title("🚗 AiCarGuy – GPT-3.5 + Domain-limited search (New openai.Client)")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.text_input("Ask me an automotive repair or a product question on godsmods.shop:")

if st.button("Submit"):
    if not user_input.strip():
        st.warning("Please enter a question.")
    else:
        reply = answer_query(user_input)
        st.session_state["history"].append((user_input, reply))

for q, a in reversed(st.session_state["history"]):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**AiCarGuy:** {a}")
    st.write("---")
