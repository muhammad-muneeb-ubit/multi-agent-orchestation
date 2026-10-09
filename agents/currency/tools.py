
from langchain.tools import tool
import requests
import time
from log import logger

logger.info("Exchange rate tool started.")
start_time = time.perf_counter()

@tool
def get_exchange_rate(
    from_currency: str,
    to_currency: str
) -> float:
    """Get the latest exchange rate between two currencies."""

    url = (
        f"https://api.frankfurter.dev/v2/"
        f"rate/{from_currency.upper()}/{to_currency.upper()}"
    )

    response = requests.get(url)
    response.raise_for_status()

    data = response.json()
    elapse = time.perf_counter() - start_time
    logger.info(f"Exchange rate tool completed in {elapse}s")
    return data["rate"]
