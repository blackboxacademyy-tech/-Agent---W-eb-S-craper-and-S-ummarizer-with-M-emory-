import streamlit as st
import requests
from bs4 import BeautifulSoup
import json
import os
from openai import OpenAI

# -----------------------------
# CONFIG
# -----------------------------

st.set_page_config(page_title="AI Web Agent", layout="centered")

client = OpenAI(api_key="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")

MEMORY_FILE = "memory.json"

# -----------------------------
# MEMORY FUNCTIONS
# -----------------------------

def load_memory():
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            return json.load(f)
    return {"history": []}

def save_memory(memory):
    with open(MEMORY_FILE, "w") as f:
        json.dump(memory, f, indent=4)

memory = load_memory()

# -----------------------------
# SCRAPER
# -----------------------------

def scrape_website(url):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")
        text = " ".join([p.get_text() for p in paragraphs])

        return text[:3000]  # limit for demo

    except Exception as e:
        return f"Error: {e}"

# -----------------------------
# SUMMARIZER
# -----------------------------

def summarize(text):
    prompt = f"Summarize this content in simple terms:\n\n{text}"

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output[0].content[0].text

# -----------------------------
# CHAT AGENT
# -----------------------------

def chat_with_memory_no_rag(query):
    past_data = memory["history"][-3:]  # last 3 summaries

    context = ""
    for item in past_data:
        context += f"URL: {item['url']}\nSummary: {item['summary']}\n\n"

    prompt = f"""
    You are an AI assistant.

    Here is some previously collected knowledge:

    {context}

    Answer the user question based on this knowledge.
    If the answer is not present, say "I don't know based on stored data."

    Question: {query}
    """

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    return response.output[0].content[0].text

# -----------------------------
# UI
# -----------------------------

st.title("🌐 Agent - W(eb) S(craper) and S(ummarizer) with M(emory)")

# -------- Scraping Section --------
st.subheader("🔍 Scrape & Summarize")

url = st.text_input("Enter website URL")

if st.button("Scrape & Summarize"):
    if url:
        st.write("🔄 Scraping...")
        content = scrape_website(url)

        st.write("🧠 Summarizing...")
        summary = summarize(content)

        st.subheader("Summary")
        st.write(summary)

        # Save to memory
        memory["history"].append({
            "url": url,
            "summary": summary
        })
        save_memory(memory)

# -------- Memory Display --------
st.subheader("📜 Past Summaries")

if memory["history"]:
    for item in memory["history"][-5:]:
        st.write(f"🔗 {item['url']}")
        st.write(item["summary"])
        st.write("---")
else:
    st.write("No memory yet.")

# -------- Chat Section --------
st.subheader("💬 Chat with Scraped Data")

user_query = st.text_input("Ask something based on stored summaries")

if st.button("Ask AI"):
    if user_query:
        answer = chat_with_memory_no_rag(user_query)
        st.write("🤖", answer)

# -------- Optional Controls --------
st.sidebar.header("⚙️ Controls")

if st.sidebar.button("Clear Memory"):
    memory = {"history": []}
    save_memory(memory)
    st.sidebar.success("Memory cleared!")