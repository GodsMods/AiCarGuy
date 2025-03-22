import streamlit as st
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from duckduckgo_search import DDGS
import numpy as np
import faiss

# Load smarter, instruction-tuned model (Gemma 2B)
generator = pipeline("text-generation", model="google/gemma-2b-it", device=-1)

# Efficient embedding model
embedder = SentenceTransformer('all-MiniLM-L6-v2')

def retrieve_context(query, num_results=3):
    with DDGS() as ddgs:
        web_results = list(ddgs.text(query + " automotive repair", max_results=5))
    if not web_results:
        return "No relevant automotive repair information found."

    docs = [f"{res['title']}: {res['body']}" for res in web_results]
    embeddings = embedder.encode(docs, convert_to_numpy=True)

    index = faiss.IndexFlatL2(embeddings.shape[1])
    index.add(embeddings)

    query_emb = embedder.encode([query])
    distances, indices = index.search(query_emb, num_results)

    return "\n".join([docs[i] for i in indices[0]])

# Streamlit UI
st.title("🚗 AiCarGuy - Advanced Automotive Chatbot")

if 'history' not in st.session_state:
    st.session_state['history'] = []

user_input = st.text_input("Ask any automotive repair or maintenance question:")

if st.button("Submit"):
    context = retrieve_context(user_input)

    prompt = f"""You are a helpful automotive assistant. Use this context to accurately answer the user's question:

Context:
{context}

Question:
{user_input}

Answer:
"""

    output = generator(prompt, max_length=500, temperature=0.7, do_sample=True)[0]['generated_text']
    reply = output.split("Answer:")[-1].strip()

    st.session_state['history'].append((user_input, reply))

for q, a in reversed(st.session_state['history']):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**AiCarGuy:** {a}")
    st.write("---")
