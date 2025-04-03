
# AiCarGuy – Automotive Chatbot

**AiCarGuy** is an automotive repair and upgrade chatbot that uses OpenAI's GPT‑3.5‑turbo to answer highly specific automotive questions. It retrieves domain-specific product info from [godsmods.shop](https://godsmods.shop) (via a domain‑restricted DuckDuckGo search) and also fetches general automotive repair details. The chatbot only answers automotive-related queries, and it maintains conversation history for follow‑up questions until the session ends.

## Features

- **High‑Quality Responses:** Uses OpenAI's GPT‑3.5‑turbo (via the new OpenAI Python client) for natural, detailed responses.
- **Domain‑Restricted Search:** Searches godsmods.shop for product info (using DuckDuckGo) and returns product links.
- **General Web Information:** Retrieves general automotive repair info using DuckDuckGo.
- **Session Memory:** Remembers conversation history so follow‑up questions are contextual.
- **Easy Embedding:** Can be embedded into your Shopify store via an iframe.

## Prerequisites

- Python 3.7 or later.
- An [OpenAI API key](https://platform.openai.com/signup). (Store it in your Streamlit Cloud secrets as `OPENAI_API_KEY`.)
- A deployed version of the app (for example, on [Streamlit Cloud](https://streamlit.io/cloud)) if you want to embed it in your Shopify store.

## Repository Structure

AiCarGuy/
├── streamlit_app.py    # Main Streamlit application code.
├── requirements.txt    # List of Python dependencies.
└── README.md           # This file.

## Installation

1. **Clone the Repository:**

   ```
   bash
   git clone https://github.com/yourusername/AiCarGuy.git
   cd AiCarGuy
```
	2.	Install Dependencies:
Make sure your requirements.txt includes:
```
streamlit
openai>=0.28.0
duckduckgo-search==3.8.0
numpy
```
Then run:
```
pip install -r requirements.txt
```


Running the App Locally

To test the app locally, run:
```
streamlit run streamlit_app.py
```
This will open a browser window where you can test the chatbot.

Setting Up OpenAI API Key

When deploying on Streamlit Cloud:
	1.	Go to your app’s Settings → Secrets.
	2.	Add a secret with the key OPENAI_API_KEY and paste your API key as its value.

Code Overview
	•	streamlit_app.py
This file includes:
	•	The new OpenAI client setup (using the latest openai.Client and chat completions).
	•	A robust automotive keyword filter to ensure only relevant questions are answered.
	•	Functions that use DuckDuckGo’s DDGS to perform:
	•	Domain‑restricted search on godsmods.shop (to find product links).
	•	General automotive repair information search.
	•	The conversation logic that builds a list of messages (including system, assistant, and user messages) to send to GPT‑3.5‑turbo.
	•	A Streamlit UI that maintains conversation history in st.session_state.

Deployment

Deploy on Streamlit Cloud
	1.	Push your repository to GitHub.
	2.	Log in to Streamlit Cloud.
	3.	Create a new app, link your GitHub repo, and deploy.
	4.	Once deployed, note the public URL for embedding.

Embedding in Your Shopify Store

To embed your chatbot on your Shopify homepage:
	1.	In your Shopify admin, navigate to Online Store > Pages and create (or edit) a page.
	2.	Switch to the HTML editor and paste this iframe snippet:

<iframe src="https://your-app-name.streamlit.app" 
        width="100%" 
        height="800" 
        frameborder="0" 
        style="border: none; overflow: hidden;">
</iframe>


	3.	Replace https://your-app-name.streamlit.app with your actual Streamlit app URL.
	4.	Save your changes.

Troubleshooting
	•	DuckDuckGo Search Errors:
If the DuckDuckGo search fails (e.g., due to rate limiting), the functions catch exceptions and return a fallback message.
	•	Memory or API Limits:
Monitor your OpenAI API usage via your OpenAI dashboard.
	•	Conversation History:
The app maintains history in st.session_state until the session ends or the user clears it.

Contributing

Feel free to open issues or submit pull requests for improvements and bug fixes.

License

This project is licensed under the MIT License.

---

### How to Use

1. **Copy and paste** the above content into a file named `README.md` in your repository.  
2. **Push** it to GitHub along with your other files.  
3. Follow the instructions to deploy your app and embed it on your Shopify homepage.
