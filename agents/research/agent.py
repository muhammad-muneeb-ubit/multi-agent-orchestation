from langgraph.graph import StateGraph, START, END, MessagesState
from config import llm
from .tools import get_research_info
from langgraph.prebuilt import ToolNode
import time
from log import logger

logger.info("Research Agent started.")
agent_start = time.perf_counter()
class State(MessagesState):
    pass

tools = [get_research_info]
llm_with_tools = llm.bind_tools(tools)

def call_llm(state:State):
    logger.info("Research Agent processing and LLM call started...")
    start = time.perf_counter()
    response = llm_with_tools.invoke(
        state["messages"]
    )
    elapsed = time.perf_counter() - start
    logger.info(f"Research Agent LLM call completed in {elapsed}s")
    return {
        "messages": [response]
    }

def should_continue(state: State):
    logger.info("Research Agent decision making started...")
    start = time.perf_counter()
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        elapsed = time.perf_counter() - start
        logger.info(f"Research Agent decision making completed in {elapsed}s")
        return "tools"
    elapsed = time.perf_counter() - start
    logger.info(f"Research Agent decision making completed in {elapsed}s")
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
logger.info(f"Research Agent completed in {elapsed}s")

# result = app.invoke({
#     "messages": [
#         {"role": "user", "content": "Get me the latest research information about RAG (Retrieval-Augmented Generation)."}
#     ]
# })

# print("result: ", result["messages"][-1].content[0].get("text"))