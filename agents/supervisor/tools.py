from langchain.tools import tool
from config import llm

@tool
def summarize_text(text: str) -> str:
    """
    Summarize the given text.
    """
    prompt = f"Please summarize the following text:\n\n{text}"
    response = llm.invoke(prompt)
    return response["text"]