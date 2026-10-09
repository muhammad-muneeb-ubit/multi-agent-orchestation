from langgraph.graph import StateGraph, START, END, MessagesState
from config import llm  
from langgraph.prebuilt import ToolNode
from.tools import suggest_testing_techniques
import time
from log import logger

logger.info("Testing Agent started.")
agent_start = time.perf_counter()

class State(MessagesState):
    pass

tools = [suggest_testing_techniques]
llm_with_tools = llm.bind_tools(tools)

def call_llm(state:State):
    logger.info("Testing Agent processing and LLM call started...")
    start = time.perf_counter()
    response = llm_with_tools.invoke(
        state["messages"]
    )
    elapsed = time.perf_counter() - start
    logger.info(f"Testing Agent LLM call completed in {elapsed}s")
    return {
        "messages": [response]
    }
    
def should_continue(state: State):
    logger.info("Testing Agent decision making started...")
    start = time.perf_counter()
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        elapsed = time.perf_counter() - start
        logger.info(f"Testing Agent decision making completed in {elapsed}s")
        return "tools"
    elapsed = time.perf_counter() - start
    logger.info(f"Testing Agent decision making completed in {elapsed}s")
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
logger.info(f"Testing Agent completed in {elapsed}s")