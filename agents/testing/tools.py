
from langchain.tools import tool
from config import llm
import time
from log import logger
logger.info("Testing tool started.")
start_time = time.perf_counter()

@tool
def suggest_testing_techniques(code: str) -> str:
    """Suggest testing techniques for the given code."""
    response = llm.invoke(
        f"Suggest testing techniques for the following code:\n{code}"
    )
    
    elapsed_time = time.perf_counter() - start_time
    logger.info(f"Testing tool completed in {elapsed_time}s")

    return response.content[0]["text"]