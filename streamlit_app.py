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
    "car","engine","brake","tire","vehicle","automotive","transmission",
    "exhaust","repair","maintenance","mod","lugnut","wheel","coolant","oil",
    "fluid","battery","spark plug","radiator","alternator","starter","ignition",
    "fuel","sensor","sierra","gmc","chevrolet","ford","honda","toyota"
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
        messages.append({"role": "system", "content": "You are a helpful automotive repair and upgrade expert. You ONLY answer automotive questions."})

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

user_input = st.text_input("Ask an automotive question or a product question on godsmods.shop:")

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
