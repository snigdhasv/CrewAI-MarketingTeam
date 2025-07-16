import os
import json
import requests
from crewai.tools import tool
from langchain_community.document_loaders import WebBaseLoader

# 🔧 Shared logic for internet search
def _run_serper_search(query: str, limit: int = 5) -> str:
    url = "https://google.serper.dev/search"
    payload = {"q": query, "num": limit}
    headers = {
        "X-API-KEY": os.getenv("SERPER_API_KEY"),
        "Content-Type": "application/json",
    }
    resp = requests.post(url, json=payload, headers=headers)
    results = resp.json().get("organic", [])
    formatted = "\n\n".join(
        f"{r['title']}\n{r['snippet']}\n{r['link']}"
        for r in results
    )
    return f"Search results for '{query}':\n\n{formatted}"


@tool("Search Internet")
def search_internet(query: str, limit: int = 5) -> str:
    """
    Search the internet using Serper API. Returns top `limit` results.
    """
    return _run_serper_search(query, limit)

@tool("Search Instagram")
def search_instagram(query: str, limit: int = 5) -> str:
    """
    Search Instagram pages via Serper limiting to site:instagram.com.
    """
    return _run_serper_search(f"site:instagram.com {query}", limit)

@tool("Open Page")
def open_page(url: str) -> str:
    """
    Load and return the content of the webpage at `url`.
    """
    from langchain_community.document_loaders import WebBaseLoader
    loader = WebBaseLoader(url)
    docs = loader.load()
    return docs[0].page_content if docs else ""

