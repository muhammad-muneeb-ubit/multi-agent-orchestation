from langchain.tools import tool
import requests
import time
from log import logger
logger.info("Weather tool started.")
start_time = time.perf_counter()

@tool
def get_weather(location: str) -> dict:
    """
    Get the current weather for a city or location.
    The location can be a city name or city with country,
    for example 'Karachi' or 'Karachi, Pakistan'.
    """

    geo_url = "https://geocoding-api.open-meteo.com/v1/search"

    geo_params = {
        "name": location,
        "count": 1,
        "language": "en",
        "format": "json"
    }

    geo_response = requests.get(
        geo_url,
        params=geo_params
    )

    geo_response.raise_for_status()

    geo_data = geo_response.json()

    if not geo_data.get("results"):
        return {
            "error": f"Location '{location}' was not found."
        }

    place = geo_data["results"][0]

    latitude = place["latitude"]
    longitude = place["longitude"]

    # 2. Get weather
    weather_url = "https://api.open-meteo.com/v1/forecast"

    weather_params = {
        "latitude": latitude,
        "longitude": longitude,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto"
    }

    weather_response = requests.get(
        weather_url,
        params=weather_params
    )

    weather_response.raise_for_status()

    weather_data = weather_response.json()

    current = weather_data["current"]
    elapsed_time = time.perf_counter() - start_time
    logger.info(f"Weather tool completed in {elapsed_time}s")

    return {
        "location": place["name"],
        "country": place.get("country"),
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "wind_speed": current["wind_speed_10m"],
        "timezone": weather_data.get("timezone")
    }
    
