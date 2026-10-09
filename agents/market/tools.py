from langchain.tools import tool
import requests
import time
from log import logger
CRYPTO_IDS = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "bnb": "binancecoin",
    "xrp": "ripple",
    "ada": "cardano",
    "doge": "dogecoin",
}


@tool
def get_market_rate(asset: str, currency: str = "pkr") -> dict:
    """
    Get the market rate of an asset against a currency.

    Examples:
    - asset="xau", currency="pkr" -> Gold to PKR
    - asset="xag", currency="pkr" -> Silver to PKR
    - asset="xcu", currency="pkr" -> Copper to PKR

    Returns the rate and basic information about the requested asset.
    """
    logger.info("Market rate tool started.")
    start_time = time.perf_counter()

    asset = asset.lower().strip()
    currency = currency.lower().strip()

    url = f"https://api.frankfurter.dev/v2/rate/{asset}/{currency}"

    response = requests.get(url, timeout=10)
    response.raise_for_status()

    data = response.json()

    asset_names = {
        "xau": "Gold",
        "xag": "Silver",
        "xcu": "Copper",
    }
    elapsed_time = time.perf_counter() - start_time
    logger.info(f"Market rate tool completed in {elapsed_time}s")
    return {
        "asset": asset_names.get(asset, asset.upper()),
        "symbol": asset.upper(),
        "currency": currency.upper(),
        "rate": data.get("rate"),
        "date": data.get("date"),
    }
    
@tool
def get_crypto_price(
    crypto: str,
    currency: str = "usd"
) -> dict:
    """
    Get the current cryptocurrency price.

    Supported examples:
    BTC, ETH, SOL, BNB, XRP, ADA, DOGE.
    """

    logger.info("crypto tool started.")
    start_time = time.perf_counter()
    crypto = crypto.lower().strip()
    currency = currency.lower().strip()

    crypto_id = CRYPTO_IDS.get(crypto, crypto)

    url = "https://api.coingecko.com/api/v3/simple/price"

    params = {
        "ids": crypto_id,
        "vs_currencies": currency
    }

    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    data = response.json()

    if crypto_id not in data:
        return {
            "error": f"Cryptocurrency '{crypto}' was not found."
        }
    elapsed_time = time.perf_counter() - start_time
    logger.info(f"crypto tool completed in {elapsed_time}s")
    return {
        "asset": crypto.upper(),
        "currency": currency.upper(),
        "price": data[crypto_id][currency]
    }