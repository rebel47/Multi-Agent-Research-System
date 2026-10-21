from langchain.tools import tool
import requests
from bs4 import BeautifulSoup
from tavily import TavilyClient
import os
from dotenv import load_dotenv
load_dotenv()
from rich import print

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))


@tool
def get_webpage_content(url_query: str) -> str:
    """
    Get the content of a webpage given its URL.

    Args:
        url_query (str): The URL of the webpage.

    Returns:
        str: The content of the webpage.
    """
    results = tavily.search(query=url_query, max_results=5)

    output = []
    for i in results["results"]:
        output.append(f"Title: {i['title']}\nURL: {i['url']}\nSnippet: {i['content'][:300]}\n\n")
    return "\n".join(output)

@tool
def scrape_url(url: str) -> str:
    """
    Scrape the content of a webpage given its URL.

    Args:
        url (str): The URL of the webpage.

    Returns:
        str: The scraped content of the webpage.
    """
    try:
        response = requests.get(url, timeout=10, headers={'User-Agent': 'Mozilla/5.0'})
        response.raise_for_status() 
        soup = BeautifulSoup(response.content, 'html.parser')
        for tag in soup(['script', 'style', 'header', 'footer', 'nav', 'aside', 'form', 'noscript']):
            tag.decompose() 
        return soup.get_text(separator=' ', strip=True)[:4000] 
    except requests.exceptions.RequestException as e:
        return f"An error occurred while trying to scrape the URL: {e}"

#print(scrape_url.invoke("https://www.bbc.com/news/articles/cr62ylj832vxo"))

#print(get_webpage_content.invoke("what is the latest research on multi-agent systems?"))