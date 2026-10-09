from agents.supervisor.agent import app

# currency api --> https://api.frankfurter.dev/v2/rate/eur/pkr 
# weather api --> get country latitude and longitude and pass it to the weather api 
# news api --> https://gnews.io/api/v4/top-headlines?category=general&apikey=f5a774657add04b7ebf201ae49db1758&lang=en&country=pk 
# country info --> https://countries.dev/alpha/pakistan 
# reseaerch api --> https://export.arxiv.org/api/query?search_query=all:RAG&max_results=5

result = app.invoke({
    "question": "What is RAG?",
    "answer": "",
    "next_agent": ""
})

print(result["answer"])