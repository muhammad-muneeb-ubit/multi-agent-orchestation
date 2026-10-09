from langchain.tools import tool
import requests

# @tool 
# def get_research_info(topic: str) -> dict:
#     """
#     Get the latest research information from arXiv.
#     This tool fetches the latest research papers related to RAG (Retrieval-Augmented Generation).
#     """

#     research_url = "https://export.arxiv.org/api/query"
    
#     research_params = {
#         "search_query": f"all:{topic}",
#         "max_results": 5
#     }

#     research_response = requests.get(
#         research_url,
#         params=research_params
#     )

#     research_response.raise_for_status()

#     research_data = research_response.text

#     return {
#         "research_info": research_data
#     }
import time
from log import logger
logger.info("Research tool started.")
start_time = time.perf_counter()

@tool
def get_research_info(topic: str) -> dict:
    """Get a short list of recent research papers about a topic."""

    research_url = "https://export.arxiv.org/api/query"

    research_params = {
        "search_query": f"all:{topic}",
        "max_results": 3
    }

    response = requests.get(
        research_url,
        params=research_params
    )

    response.raise_for_status()

    # Parse XML
    import xml.etree.ElementTree as ET

    root = ET.fromstring(response.text)

    papers = []

    for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
        title = entry.find("{http://www.w3.org/2005/Atom}title")
        summary = entry.find("{http://www.w3.org/2005/Atom}summary")
        link = entry.find("{http://www.w3.org/2005/Atom}id")

        papers.append({
            "title": title.text.strip() if title is not None else "",
            "summary": summary.text.strip()[:500] if summary is not None else "",
            "url": link.text.strip() if link is not None else ""
        })
    elapsed_time = time.perf_counter() - start_time
    logger.info(f"Research tool completed in {elapsed_time}s")
    return {
        "papers": papers
    }