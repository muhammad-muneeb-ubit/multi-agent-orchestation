from langchain.tools import tool
import requests
import time
from log import logger
logger.info("Weather tool started.")
start_time = time.perf_counter()
@tool
def get_news(category: str, country: str) -> dict:
    """
    Get the latest news for a specific category and country.
    The category can be 'general', 'business', 'entertainment', 'health', 'science', 'sports', or 'technology'.
    The country should be a two-letter country code, for example 'us' for the United States or 'pk' for Pakistan.
    """

    api_key = "f5a774657add04b7ebf201ae49db1758"
    url = f"https://gnews.io/api/v4/top-headlines?category={category}&apikey={api_key}&lang=en&country={country}"

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    elapsed_time = time.perf_counter() - start_time
    logger.info(f"News tool completed in {elapsed_time}s")
    return data
