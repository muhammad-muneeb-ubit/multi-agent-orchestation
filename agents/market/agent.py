from langgraph.graph import StateGraph, START, END, MessagesState
from config import llm  
from langgraph.prebuilt import ToolNode
from.tools import get_crypto_price, get_market_rate
import time
from log import logger

logger.info("Market Agent started.")
agent_start = time.perf_counter()

class State(MessagesState):
    pass
logger.info("Market Agent initialized.")

tools = [get_crypto_price, get_market_rate]
llm_with_tools = llm.bind_tools(tools)

def call_llm(state:State):
    logger.info("Market Agent processing and LLM call started...")
    start = time.perf_counter()
    response = llm_with_tools.invoke(
        state["messages"]
    )
    elapsed = time.perf_counter() - start
    logger.info(f"Market Agent LLM call completed in {elapsed}s")
    return {
        "messages": [response]
    }
    
def should_continue(state: State):
    logger.info("Market Agent decision making started...")
    start = time.perf_counter()
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        elapsed = time.perf_counter() - start
        logger.info(f"Market Agent decision making completed in {elapsed}s")
        return "tools"
    elapsed = time.perf_counter() - start
    logger.info(f"Market Agent decision making completed in {elapsed}s")
    return "end"

graph = StateGraph(State)
tools_node = ToolNode(tools=tools)

graph.add_node("llm", call_llm)
graph.add_node("tools", tools_node)


graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", should_continue, {"tools": "tools", "end": END})
graph.add_edge("tools", "llm")

app = graph.compile()

elapsed = time.perf_counter() - agent_start
logger.info(f"Market Agent completed in {elapsed}s")