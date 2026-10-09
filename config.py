from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatGoogleGenerativeAI(
    google_api_key=os.getenv("GEMINI_API_KEY"),
    model=os.getenv("GEMINI_MODEL"),
    temperature= 0,
    max_output_tokens=500
)