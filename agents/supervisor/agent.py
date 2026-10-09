from tracemalloc import start
from typing import Literal, TypedDict
from langgraph.graph import StateGraph, START, END, MessagesState
from langchain_core.messages import HumanMessage
from config import llm
from .tools import summarize_text
from log import logger
import time

from langgraph.prebuilt import ToolNode
from agents.research.agent import app as research_agent
from agents.countryInfo.agent import app as country_agent
from agents.news.agent import app as news_agent
from agents.weather.agent import app as weather_agent
from agents.currency.agent import app as currency_agent
from agents.coding.agent import app as coding_agent
from agents.testing.agent import app as testing_agent
from agents.market.agent import app as market_agent

supervisor_start = time.perf_counter()
logger.info("Supervisor started.")

tools = [summarize_text]
tools_node = ToolNode(tools=tools)

class State(MessagesState):
    next_agent: str
    
def get_text(response):

    if isinstance(response.content, str):
        return response.content

    if isinstance(response.content, list):
        for item in response.content:
            if isinstance(item, dict) and item.get("text"):
                return item["text"]

    return ""
    
def supervisor(state: State):
    logger.info("Supervisor processing...")
    start = time.perf_counter()
    logger.info("Supervisor received message ")
    messages = state["messages"][-1].content

    start = time.perf_counter()
    logger.info("Supervisor decision making started, LLM call started.")
    response = llm.invoke(
        f"""
        You are a supervisor responsible for routing user requests.

        Choose exactly ONE of these agents:

        - weather
        - news
        - currency
        - research
        - coding
        - testing
        - market
        - country

        Agent responsibilities:

        weather:
        Questions about current weather, temperature, forecasts,
        rain, humidity, etc.

        news:
        Questions asking for latest news or current events.

        currency:
        Questions about exchange rates and currency conversion.

        research:
        Questions about research papers, academic research,
        RAG, AI research, machine learning research, etc.

        country:
        Questions about country information such as capital,
        population, currency, region, borders, etc.

        coding:
        Questions about coding, programming, code generation,
        code explanation, code fixing, code execution, etc.

        testing:
        Questions about differnt testing techniques, testing strategies, testing tools, etc.

        market:
        Questions about rates of change in gold, silver, copper, crypto, stock market, commodities, etc.

        country:
        Questions about country information such as capital,
        population, currency, region, borders, etc.

        User request:
        {messages}

        Respond with ONLY the agent name.
        """
    )
    elapsed = time.perf_counter() - start
    logger.info(f"Supervisor LLM call completed in {elapsed}s")

    decision = get_text(response).strip().lower()

    logger.info("Supervisor decision: " + decision)
    elapsed = time.perf_counter() - start
    logger.info(f"Supervisor decision making completed in {elapsed}s")


    return {
        "next_agent": decision
    }
     
def route_supervisor(state: State) -> Literal[ "weather", "news", "currency", "research", "country", "coding", "testing", "market"]:
    logger.info("Routing to next agent...")
    return state["next_agent"]

graph = StateGraph(State)

graph.add_node("supervisor", supervisor)
graph.add_node("tools", tools_node)
graph.add_node("weather", weather_agent)
graph.add_node("news", news_agent)
graph.add_node("currency", currency_agent)
graph.add_node("research", research_agent)
graph.add_node("country", country_agent)
graph.add_node("coding", coding_agent)
graph.add_node("testing", testing_agent)
graph.add_node("market", market_agent)

start = time.perf_counter()
logger.info("Graph started.")
graph.add_edge(START, "supervisor")
elapsed = time.perf_counter() - start
logger.info(f"Graph initialized in {elapsed}s")


start = time.perf_counter()
logger.info("Graph execution started.")
graph.add_conditional_edges("supervisor", route_supervisor, {
    "weather": "weather",
    "news": "news",
    "currency": "currency",
    "research": "research",
    "coding": "coding",
    "testing": "testing",
    "market": "market",
    "country": "country"
})
elapsed = time.perf_counter() - start
logger.info(f"Graph execution started in {elapsed}s")


start = time.perf_counter();
logger.info("Graph execution completed.")
graph.add_edge("weather", END)
graph.add_edge("news", END)
graph.add_edge("currency", END)
graph.add_edge("research", END)
graph.add_edge("coding", END)
graph.add_edge("testing", END)
graph.add_edge("market", END)
graph.add_edge("country", END)
elapsed = time.perf_counter() - start
logger.info(f"Graph execution completed in {elapsed}s")


app = graph.compile()

result = app.invoke({
    "messages": [
        # HumanMessage(content="Tell me about Bitcoin. How much is it worth?")
        # HumanMessage(content="temperature in karachi?")
        HumanMessage(content="What is the temperature in clifton, karachi? Also tell the any special news about karachi today.")
        # HumanMessage(content="What is the current price of gold per tola in pakistan in pkr and ?")
        # HumanMessage(content="top 5 updates of pakistan specially karachi?")
    ]
})
# result = app.invoke({
#     "messages": [
#         HumanMessage(content='''give me testing techniques for below code,
#                      import requests

# def get_weather(city):
#     # wttr.in provides a simple JSON API
#     url = f"https://wttr.in/{city}?format=j1"
    
#     try:
#         response = requests.get(url)
#         response.raise_for_status()
#         data = response.json()
        
#         # Extracting relevant information
#         current_condition = data['current_condition'][0]
#         temp = current_condition['temp_C']
#         desc = current_condition['weatherDesc'][0]['value']
        
#         print(f"Current weather in {city}:")
#         print(f"Temperature: {temp}°C")
#         print(f"Condition: {desc}")
        
#     except Exception as e:
#         print(f"Error fetching weather: {e}")
#                      ''')
#     ]
# })


elapsed = time.perf_counter() - supervisor_start
logger.info(f"Supervisor completed in {elapsed}s")
print("\n",result["messages"][-1].content[0].get("text"))