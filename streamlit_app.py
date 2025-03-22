import streamlit as st
import openai

openai.api_key = st.secrets["OPENAI_API_KEY"]  # We'll store the key in Streamlit secrets

st.title("🚗 AiCarGuy – OpenAI Edition")

if "history" not in st.session_state:
    st.session_state["history"] = []

user_input = st.text_input("Ask any automotive repair or maintenance question:")

if st.button("Submit"):
    if not user_input.strip():
        reply = "Please enter a question."
    else:
        # Call OpenAI ChatCompletion
        messages = [
            {"role": "system", "content": "You are a helpful automotive repair expert."},
        ]
        # Add conversation history
        for q, a in st.session_state["history"]:
            messages.append({"role": "user", "content": q})
            messages.append({"role": "assistant", "content": a})

        # Add current user query
        messages.append({"role": "user", "content": user_input})

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            temperature=0.7
        )

        reply = response["choices"][0]["message"]["content"]

    st.session_state["history"].append((user_input, reply))

# Display chat history
for q, a in reversed(st.session_state["history"]):
    st.markdown(f"**You:** {q}")
    st.markdown(f"**AiCarGuy:** {a}")
    st.write("---")
