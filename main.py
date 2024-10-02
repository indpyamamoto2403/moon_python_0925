from fastapi import FastAPI
from get_prompt import GetPrompt
from search_page import SearchPage
from html_parser import HTMLParser
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import requests
from dotenv import load_dotenv
import os
load_dotenv()

class URLQuery(BaseModel):
    url_path: str

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

prompt = GetPrompt(api_key = os.getenv("API_KEY"), endpoint = os.getenv("ENDPOINT"))
search_bot = SearchPage(subscription_key = os.getenv("SUBSCRIPTION_KEY") , search_endpoint = os.getenv("SEARCH_ENDPOINT"))
parser = HTMLParser()
print("API_KEY:")
@app.get("/")
def read_root():
    return {"Hello": "AI + FastAPI World"}

@app.get("/question/{question}")
def index(question: str):
    """
    これには、質問を受け取り、回答を返すエンドポイントが含まれます。
    """
    answer = prompt._question_answer(question)
    return {"question": question, "answer": answer}


@app.post("/url_content")
def index(url_query: URLQuery):
    """
    これには、URLを受け取り、URL本文を返すエンドポイントが含まれます。
    """
    url_path = url_query.url_path
    text_content = parser.fetch_content_from_url(url_path)
    return text_content

@app.post("/url_query")
def index(url_query: URLQuery):
    """
    これには、URLを受け取り、回答を返すエンドポイントが含まれます。
    """
    url_path = url_query.url_path
    answer = prompt.get_answer_by_url(url_path)
    return answer

@app.get("/keyword_query/{keyword}")
def index(keyword: str):
    """
    これにはキーワードを受け取り、回答を返すエンドポイントが含まれます
    """
    answer = prompt.get_answer_by_keyword(keyword)
    return answer

@app.get("/search/{keyword}")
def index(keyword: str):
    """
    キーワードからsearch API経由で上位ヒットしたURLを取得し、
    それをBeautiful Soupで解析、要約まで行うエンドポイント
    """
    url = search_bot.get_search_url_by_keyword(keyword)
    text_content = parser.fetch_content_from_url(url)
    search_results = prompt.summarize_content(text_content)
    return {"keyword": keyword, "url": url, "summary": search_results}

@app.get("/search_url/{keyword}")
def index(keyword):
    url = search_bot.get_search_url_by_keyword(keyword)
    return url

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)