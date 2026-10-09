from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from .tools import get_weather
from config import llm 
import time
from log import logger
logger.info("Weather Agent started.")
agent_start = time.perf_counter()

class State(MessagesState):
    pass
    
tools = [get_weather]
llm_with_tools = llm.bind_tools(tools)

def call_llm(state:State):
    logger.info("Weather Agent processing and LLM call started...")
    start = time.perf_counter()
    response = llm_with_tools.invoke(
        state["messages"]
    )
    elapsed = time.perf_counter() - start
    logger.info(f"Weather Agent LLM call completed in {elapsed}s")
    return {
        "messages": [response]
    }
    
def should_continue(state: State):
    logger.info("Weather Agent decision making started...")
    start = time.perf_counter()
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        elapsed = time.perf_counter() - start
        logger.info(f"Weather Agent decision making completed in {elapsed}s")
        return "tools"
    elapsed = time.perf_counter() - start
    logger.info(f"Weather Agent decision making completed in {elapsed}s")
    return "end"

tools_node = ToolNode(tools=tools)

graph = StateGraph(State)

graph.add_node("llm", call_llm)
graph.add_node("tools", tools_node)

graph.add_edge(START, "llm")
graph.add_conditional_edges("llm", should_continue, {"tools": "tools", "end": END})
graph.add_edge("tools", "llm")

app = graph.compile()

elapsed = time.perf_counter() - agent_start
logger.info(f"Weather Agent completed in {elapsed}s")
# result = app.invoke({
#     "messages": [
#         {"role": "user", "content": "What is the weather in Clifton, Karachi?"}
#     ]
# })

# print("Final result", result["messages"][-1].content[0].get("text"))