import streamlit as st
from transformers import pipeline, AutoTokenizer, AutoModel
from duckduckgo_search import DDGS
import numpy as np
import faiss
import torch

# Load DistilGPT2
generator = pipeline("text-generation", model="distilgpt2", device=-1)

# Load tiny semantic embedding model
embed_model_id = "sentence-transformers/all-MiniLM-L6-v2"
tokenizer = AutoTokenizer.from_pretrained(embed_model_id)
model = AutoModel.from_pretrained(embed_model_id)

def is_automotive_query(query):
    keywords = ["car", "engine", "brake", "tire", "vehicle", "automotive",
                "transmission", "exhaust", "repair", "maintenance",
                "mod", "lugnut", "wheel", "coolant", "oil", "fluid",
                "battery", "spark plug", "radiator", "alternator",
                "starter", "ignition", "fuel", "sensor", "sierra", "gmc", "chevrolet", "ford", "honda", "toyota"]
    query = query.lower()
    return any(keyword in query for keyword in keywords)

def get_embedding(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    embedding = outputs.last_hidden_state.mean(dim=1)
    return embedding[0].cpu().numpy()

def retrieve_context(query, num_results=3):
    web_results = ddg(query + " automotive repair", max_results=5)
    if not web_results:
        return "No relevant automotive repair information found."

    docs = [f"{res['title']}: {res['body']}" for res in web_results]

    doc_embeddings = np.vstack([get_embedding(doc) for doc in docs])
    index = faiss.IndexFlatL2(doc_embeddings.shape[1])
    index.add(doc_embeddings)

    query_emb = get_embedding(query).reshape(1, -1)
    distances, indices = index.search(query_emb, num_results)

    context = "\n".join([docs[i] for i in indices[0]])
    return context.strip()

# Streamlit UI
st.title("🚗 AiCarGuy - Automotive Chatbot")

if 'history' not in st.session_state:
    st.session_state['history'] = []

user_input = st.text_input("Ask any automotive repair or maintenance question:")

if st.button("Submit"):
    if not is_automotive_query(user_input):
        reply = "I specialize in automotive repair. Please ask about cars, engines, parts, etc."
    else:
        context = retrieve_context(user_input)
        prompt = f"Automotive Repair Information:\n{context}\nUser: {user_input}\nAnswer:"
        output = generator(prompt, max_length=150, do_sample=True, temperature=0.8)[0]["generated_text"]
        reply = output.split("Answer:")[-1].strip() if "Answer:" in output else output.strip()

    st.session_state['history'].append((user_input, reply))

for question, answer in reversed(st.session_state['history']):
    st.markdown(f"**You:** {question}")
    st.markdown(f"**AiCarGuy:** {answer}")
    st.write("---")
