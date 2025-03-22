import streamlit as st
import openai
import pandas as pd
import numpy as np
import faiss
from duckduckgo_search import DDGS
import os

############################
# 1. Setup & Configuration
############################
st.set_page_config(page_title="AiCarGuy – GPT-3.5 Chatbot", layout="wide")

# Retrieve your OpenAI key from Streamlit secrets
openai.api_key = st.secrets["OPENAI_API_KEY"]

# Domain filter keywords
AUTOMOTIVE_KEYWORDS = [
    "car","engine","brake","tire","vehicle","automotive",
    "transmission","exhaust","repair","maintenance","mod","lugnut","wheel",
    "coolant","oil","fluid","battery","spark plug","radiator","alternator",
    "starter","ignition","fuel","sensor","sierra","gmc","chevrolet","ford","honda","toyota"
]

############################
# 2. Product Catalog
############################
# We load a CSV of your godsmods.shop products
# Format: product_name, keywords, product_url
products_df = pd.read_csv("products.csv")  # Make sure this file is in the same directory

def find_relevant_products(user_query):
    """
    Very simple approach: if user_query contains any 'keyword' from the CSV,
    return the product_name + product_url. We can refine with a better match approach if needed.
    """
    user_lower = user_query.lower()
    matched_products = []
    for _, row in products_df.iterrows():
        product_keywords = [k.strip().lower() for k in row["keywords"].split(",")]
        if any(k in user_lower for k in product_keywords):
            matched_products.append((row["product_name"], row["product_url"]))
    return matched_products

############################
# 3. DuckDuckGo Web Search
############################
def retrieve_web_info(query, max_results=5):
    with DDGS() as ddgs:
        results = list(ddgs.text(query, max_results=max_results))
    if not results:
        return "No relevant info found from the web."
    # Combine titles & bodies
    combined = ""
    for r in results:
        title = r.get("title","")
        body = r.get("body","")
        combined += f"{title}: {body}\n"
    return combined.strip()

############################
# 4. GPT-3.5 Chat
############################
def call_openai_chat(messages):
    """
    messages: a list of dicts with 'role' and 'content'
    """
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages,
        temperature=0.7
    )
    return response["choices"][0]["message"]["content"]

def is_automotive_query(query):
    q_lower = query.lower()
    return any(k in q_lower for k in AUTOMOTIVE_KEYWORDS)

############################
# 5. The main logic
############################
def answer_query(user_query):
    # 5A. Domain check
    if not is_automotive_query(user_query):
        return "I only handle automotive repair or upgrade questions. Please ask about cars, engines, parts, etc."

    # 5B. Web retrieval
    # e.g. "my 2000 GMC sierra water pump"
    # We'll add "automotive repair" to ensure results
    web_snippet = retrieve_web_info(user_query + " automotive repair", max_results=5)

    # 5C. Product linking
    matched = find_relevant_products(user_query)
    product_info = ""
    if matched:
        # If we found some relevant products, mention them
        product_info = "I found these matching products on godsmods.shop:\n"
        for name, url in matched:
            product_info += f"- {name}: {url}\n"

    # 5D. Build the final system+user messages for GPT-3.5
    messages = [
        {"role": "system", "content": "You are a helpful automotive repair and upgrade expert. You ONLY answer automotive questions, referencing the user's query, the web snippet, and the product links if relevant."},
        {"role": "assistant", "content": f"Here is some background web info:\n{web_snippet}\n\nHere are possible relevant products:\n{product_info}"},
        {"role": "user", "content": user_query}
    ]
    # 5E. Call GPT-3.5
    final_answer = call_openai_chat(messages)
    return final_answer

############################
# 6. Streamlit UI
############################
st.title("🚗 AiCarGuy – GPT-3.5 with Web & godsmods.shop Links")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.text_input("Ask me an automotive repair/upgrade question:")

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
