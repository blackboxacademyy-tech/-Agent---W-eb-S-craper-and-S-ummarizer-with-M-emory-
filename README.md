# Agent LLM Tutorial

## Overview

This repository contains a small AI agent tutorial built with Python, Streamlit, BeautifulSoup, and OpenAI. The main app (`memory.py`) scrapes webpage content, summarizes it with an LLM, and stores summaries in a local JSON memory file. It also provides a simple chat interface that answers questions based on stored summaries.

## Key Features

- Web page scraping using `requests` and `BeautifulSoup`
- Content summarization via OpenAI Responses API (`gpt-4.1-mini`)
- Local memory persistence in `memory.json`
- Streamlit UI for scraping, summarizing, and conversational querying

## Repository Structure

- `memory.py` - Main Streamlit app for web scraping, summarization, memory storage, and chat
- `memory.json` - Local memory store for saved URL summary history

## Prerequisites

- Python 3.10+ recommended
- An OpenAI API key
- Internet access for scraping external websites and calling the OpenAI API

## Installation

1. Clone or open the repository in your workspace.
2. Create a Python virtual environment (recommended):

```bash
python -m venv .venv
```

3. Activate the virtual environment:

- Windows PowerShell:
```powershell
.\.venv\Scripts\Activate.ps1
```
- Windows Command Prompt:
```cmd
.\.venv\Scripts\activate.bat
```

4. Install required packages:

```bash
pip install streamlit requests beautifulsoup4 openai
```

## Configuration

The app currently uses a hardcoded OpenAI API key inside the Python files. For a safer setup, replace the API key usage with an environment variable or secure config file.

Example environment variable approach:

```bash
setx OPENAI_API_KEY "your_api_key_here"
```

Then update the code to read `OPENAI_API_KEY` from `os.environ` instead of hardcoding it.

## Running the Streamlit App

From the repository root:

```bash
streamlit run memory.py
```

Open the URL printed by Streamlit in your browser. The app provides:

- A field to enter a website URL
- A button to scrape and summarize content
- A view of the most recent saved summaries
- A chat input to ask questions based on stored data
- A sidebar button to clear memory

## How It Works

1. `memory.py` loads or creates `memory.json` to store past summaries.
2. The scraper fetches page HTML and extracts `<p>` paragraph text.
3. The text is truncated and passed to OpenAI for summarization.
4. Summaries are appended to memory and displayed in the UI.
5. The chat section builds a prompt from the latest stored summaries and asks OpenAI for an answer.

## Notes

- The current implementation limits scraped text to the first 3000 characters for demo purposes.
- The chat prompt is built from the last 3 stored summaries only.
- If you want production-ready use, move the API key out of source code and handle scraping and prompt generation more robustly.

## Improvements

Possible next steps:

- Add environment variable support for all API keys
- Improve HTML extraction to avoid navigation text and menus
- Add error handling for invalid URLs and failed API calls
- Implement retrieval-augmented generation (RAG) for better chat accuracy
- Add unit tests for scraper and memory functions

## License

This project is provided as a tutorial sample. Adapt and extend it for your own experiments.
