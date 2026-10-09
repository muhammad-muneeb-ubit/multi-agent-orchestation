from langgraph.graph import StateGraph, START, END, MessagesState
from langgraph.prebuilt import ToolNode
from .tools import execute_python_code, generate_code, explain_code, fix_code
from config import llm
from log import logger
import time

agent_start = time.perf_counter()
logger.info("Coding agent started.")
class State(MessagesState):
    pass

tools = [execute_python_code, generate_code, explain_code, fix_code]
llm_with_tools = llm.bind_tools(tools)

def call_llm(state:State):
    logger.info("coding agent processing started...")
    start = time.perf_counter()
    logger.info("coding agent LLM call started.")
    response = llm_with_tools.invoke(
        state["messages"]
    )
    elapsed = time.perf_counter() - start
    logger.info(f"coding agent LLM call completed in {elapsed}s")
    return {
        "messages": [response]
    }   
    
def should_continue(state: State):
    logger.info("coding agent decision making started...")
    start = time.perf_counter()
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        elapsed = time.perf_counter() - start
        logger.info(f"coding agent decision making completed in {elapsed}s")
        return "tools"
    elapsed = time.perf_counter() - start
    logger.info(f"coding agent decision making completed in {elapsed}s")
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
logger.info(f"Coding agent completed in {elapsed}s")