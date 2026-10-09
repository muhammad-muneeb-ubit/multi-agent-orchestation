
from langchain.tools import tool
from config import llm
import time
from log import logger

@tool
def generate_code(prompt: str) -> str:
    """Generate code based on a given prompt."""
    logger.info("Generate code tool started.")
    start_time = time.perf_counter()
    response = llm.invoke(
        f"Generate code for the following prompt:\n{prompt}"
    )
    elapsed_time = time.perf_counter() - start_time
    logger.info(f"Generate code tool completed in {elapsed_time}s")
    return response.content[0]["text"]

@tool
def explain_code(code: str) -> str:
    """Explain the given code."""
    logger.info("Explain code tool started.")
    start_time = time.perf_counter()
    response = llm.invoke(
        f"Explain the following code:\n{code}"
    )
    elapsed_time = time.perf_counter() - start_time
    logger.info(f"Explain code tool completed in {elapsed_time}s")
    return response.content[0]["text"]

@tool
def fix_code(code: str) -> str:
    """Fix the given code."""
    logger.info("Fix code tool started.")
    start_time = time.perf_counter()
    response = llm.invoke(
        f"Fix the following code:\n{code}"
    )
    elapsed_time = time.perf_counter() - start_time
    logger.info(f"Fix code tool completed in {elapsed_time}s")
    return response.content[0]["text"]

@tool
def execute_python_code(code: str) -> str:
    """Execute Python code and return the output."""
    logger.info("Execute Python code tool started.")
    start_time = time.perf_counter()
    response = llm.invoke(
            f"Execute the following Python code:\n{code}"
        )
    elapsed_time = time.perf_counter() - start_time
    logger.info(f"Execute Python code tool completed in {elapsed_time}s")
    return response.content[0]["text"]
    