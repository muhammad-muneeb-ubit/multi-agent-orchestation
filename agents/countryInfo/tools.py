
from langchain.tools import tool
import requests
import time
from log import logger

logger.info("Country info tool started.")
start_time = time.perf_counter()
@tool
def get_country_info(country: str) -> dict:
    """Get basic information about a country by its ISO 3166 code like 'PK' for Pakistan."""

    url = f"https://countries.dev/alpha/{country}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()
    elapsed_time = time.perf_counter() - start_time
    logger.info(f"Country info tool completed in {elapsed_time}s")
    return {
    "name": data.get("name"),
    "capital": data.get("capital"),
    "region": data.get("region"),
    "subregion": data.get("subregion"),
    "population": data.get("population"),
    "area": data.get("area"),
    "languages": [
        language.get("name")
        for language in data.get("languages", [])
    ],
    "timezones": data.get("timezones", []),
    "borders": data.get("borders", []),
    "independent": data.get("independent"),
}
    
    