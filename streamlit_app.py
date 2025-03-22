import streamlit as st
from transformers import pipeline
from sentence_transformers import SentenceTransformer
from duckduckgo_search import DDGS
import numpy as np
import faiss

# Use Flan-T5-Small for instruction-tuned Q&A
generator = pipeline("text2text-generation", model="google/flan-t5-small", device=-1)

# Use a small sentence-transformers model for retrieval
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

    query_emb = embedder.encode([query], convert_to_numpy=True)
    distances, indices = index.search(query_emb, num_results)

    return "\n".join([docs[i] for i in indices[0]])

st.title("🚗 AiCarGuy - Automotive Chatbot (Flan-T5)")

if 'history' not in st.session_state:
    st.session_state['history'] = []

user_input = st.text_input("Ask any automotive repair or maintenance question:")

if st.button("Submit"):
    if not user_input.strip():
        reply = "Please ask an automotive-related question."
    else:
        # Retrieve relevant context
        context = retrieve_context(user_input)
        # Build a prompt for Flan-T5
        prompt = f"""Context:
{context}

User question: {user_input}
Answer in a helpful, concise manner:
"""
        # Generate the response
        output = generator(prompt, max_length=200, temperature=0.7, do_sample=True)
        reply = output[0]['generated_text']

    st.session_state['history'].append((user_input, reply))

for q, a in reversed(st.session_state['history']):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**AiCarGuy:** {a}")
    st.write("---")
