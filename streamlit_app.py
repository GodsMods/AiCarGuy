import streamlit as st
import openai
from duckduckgo_search import DDGS
import re

st.set_page_config(page_title="AiCarGuy – GPT-3.5 + Domain Search", layout="wide")

# 1. Retrieve your OpenAI key from secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

AUTOMOTIVE_KEYWORDS = [
    "car","engine","brake","tire","vehicle","automotive","transmission",
    "exhaust","repair","maintenance","mod","lugnut","wheel","coolant","oil",
    "fluid","battery","spark plug","radiator","alternator","starter","ignition",
    "fuel","sensor","sierra","gmc","chevrolet","ford","honda","toyota"
]

def is_automotive_query(query):
    q_lower = query.lower()
    return any(k in q_lower for k in AUTOMOTIVE_KEYWORDS)

def domain_search_godsmods(query):
    """
    Search only site:godsmods.shop for relevant product links.
    Return a short string with the top link found, or a note if none found.
    """
    with DDGS() as ddgs:
        results = list(ddgs.text(f"site:godsmods.shop {query}", max_results=3))
    if not results:
        return "No product link found for that query on godsmods.shop."
    
    # Typically the first result is the best. We'll return the title + link if possible.
    # Some results might have 'href' or 'body' with the link
    link_info = ""
    for r in results:
        # The duckduckgo_search text results usually have 'title' and 'body'
        # but might not have an explicit 'href'. We'll try to parse the link from the body if present
        title = r.get("title","")
        body = r.get("body","")
        # Attempt to find a link in the body text
        url_match = re.search(r'(https?://[^\s]+)', body)
        if url_match:
            link = url_match.group(1)
            link_info += f"{title}: {link}\n"
        else:
            # If no direct link in body, just store the text
            link_info += f"{title}: {body}\n"
    return link_info.strip() if link_info else "No direct product link found."

def general_web_snippet(query):
    """
    General automotive info search (not domain restricted).
    """
    with DDGS() as ddgs:
        results = list(ddgs.text(query + " automotive repair", max_results=3))
    if not results:
        return "No general automotive info found."
    snippet = ""
    for r in results:
        snippet += f"{r.get('title','')}: {r.get('body','')}\n"
    return snippet.strip()

def call_gpt35(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"]

def answer_query(user_query):
    # 1) Domain check
    if not is_automotive_query(user_query):
        return "I only answer automotive repair or upgrade questions. Please ask something car-related."

    # 2) domain-limited search for product link
    product_links = domain_search_godsmods(user_query)

    # 3) general automotive snippet
    web_info = general_web_snippet(user_query)

    # 4) Build messages for GPT
    messages = [
        {"role": "system", "content": "You are a helpful automotive repair and upgrade expert. You ONLY answer automotive questions."},
        {"role": "assistant", "content": f"Here is some product info from godsmods.shop:\n{product_links}\n\nHere is some general automotive web info:\n{web_info}"},
        {"role": "user", "content": user_query}
    ]
    # 5) GPT-3.5
    return call_gpt35(messages)

st.title("🚗 AiCarGuy – GPT-3.5 + Domain-limited search for godsmods.shop")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.text_input("Ask about automotive repair or a product on godsmods.shop:")

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
