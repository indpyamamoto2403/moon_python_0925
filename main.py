import os
from fastapi import FastAPI, Query, Path
from get_prompt import GetPrompt
from search_page import SearchPage
from html_parser import HTMLParser
from utils import TextSplitter
from fastapi.middleware.cors import CORSMiddleware
import requests
from image_responder import ImageResponder
from get_vector import EmbeddingProcessor
from dotenv import load_dotenv
import uvicorn
from ResponseGetter import ResponseGetter, RagResponseGetter
from URLQuery import URLQuery
from dataset import *
from openai import AzureOpenAI

load_dotenv()
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)

split_chunk_size = 3000
split_overlap = 0

prompt_getter = GetPrompt(api_key = os.getenv("API_KEY"), endpoint = os.getenv("ENDPOINT"))
search_bot = SearchPage(subscription_key = os.getenv("SUBSCRIPTION_KEY") , search_endpoint = os.getenv("SEARCH_ENDPOINT"))
parser = HTMLParser()

#ベクトル化に関するクライアントを初期化
embedding_client = AzureOpenAI(
            api_key=os.getenv('EMBEDDING_API_KEY'),  
            api_version="2024-06-01",
            azure_endpoint=os.getenv('EMBEDDING_ENDPOINT'), )
embedding_processor = EmbeddingProcessor(embedding_client)


response_getter = ResponseGetter(prompt_getter, split_chunk_size, split_overlap)
rag_response_getter = RagResponseGetter(prompt_getter, split_chunk_size, split_overlap, embedding_processor)

image_responder = ImageResponder(api_key = os.getenv("API_KEY"), endpoint = os.getenv("ENDPOINT"))

@app.get("/")
def read_root():
    return {"Hello": "AI FastAPI World"}

@app.post("/")
def index(val:str):
    return {"Hello": val}

@app.get("/question/{question}")
def index(question: str):
    """
    これには、質問を受け取り、回答を返すエンドポイントが含まれます。
    """
    answer = prompt_getter._question_answer(question)
    return (question, answer)

@app.post("/question")
def index(question: str):
    """
    これには、質問を受け取り、回答を返すエンドポイントが含まれます。
    """
    answer = prompt_getter._question_answer(question)
    return {"question": question, "answer": answer}


@app.get("/question_answer_by_split")
def index(arg_prompt: str, content: str):
    '''
    クエリ文字列としてプロンプトを受取、文章に分割し、それぞれに対してプロンプトを実行し、統合プロンプトを返す
    '''
    result: SummarizationDataset = response_getter.get_summary_by_prompt_content(arg_prompt, content)
    return result

@app.post("/question_answer_by_image")
def index(prompt: str, encoded_image: str):
    """
    これには、エンコードされた画像を受け取り、回答を返すエンドポイントが含まれます。
    """
    answer = image_responder._question_answer(prompt, encoded_image)
    print(answer)
    print(type(answer))
    return answer

@app.get("/question_answer_by_rag")
def index(arg_prompt: str, content: str):
    '''
    クエリ文字列としてプロンプトを受取、文章に分割し、それぞれに対してベクトル化を行い、コサイン類似度の高い文章を選択し
    統合分を返す
    '''
    result: SummarizationDataset = rag_response_getter.get_summary_by_rag(arg_prompt, content)
    return result

@app.post("/url_content")
def index(url: str):
    """
    これには、URLを受け取り、URL本文を返すエンドポイントが含まれます。
    """
    text_content = parser.fetch_content_from_url(url)
    return text_content

@app.post("/url_query")
def index(url_query: URLQuery):
    """
    これには、URLを受け取り、回答を返すエンドポイントが含まれます。
    """
    url_path = url_query.url_path
    answer = prompt_getter.get_answer_by_url(url_path)
    return answer

@app.get("/keyword_query/{keyword}")
def index(keyword: str):
    """
    これにはキーワードを受け取り、回答を返すエンドポイントが含まれます.
    """
    answer = prompt_getter.get_answer_by_keyword(keyword)
    return answer

@app.get("/search/{keyword}")
def index(keyword: str):
    """
    キーワードからsearch API経由で上位ヒットしたURLを取得し、
    それをBeautiful Soupで解析、要約まで行うエンドポイント
    """
    url = search_bot.get_search_url_by_keyword(keyword)
    text_content = parser.fetch_content_from_url(url)
    search_results = prompt_getter.summarize_content(text_content)
    return {"keyword": keyword, "url": url, "summary": search_results}

@app.get("/search_url/{keyword}")
def index(keyword):
    url = search_bot.get_search_url_by_keyword(keyword)
    return url

@app.get("/news")
def index(page_num : int = Query(3), keyword1: str = Query(None),  keyword2: str = Query(None),keyword3: str = Query(None)):
    '''
    ニュース検索APIを利用して、ニュース記事を要約する
    引数の説明:
    page: 検索するページ数
    keyword1: 検索キーワード1
    keyword2: 検索キーワード2
    keyword3: 検索キーワード3
    '''
    const_prompt = "次のニュース記事を要約してください"
    try:
        #すべてが詰まったオブジェクト。EntireDataset型を受け取る
        data:EntireDataset = EntireDataset(input_dataset=InputDataset(keyword1=keyword1, keyword2=keyword2, keyword3=keyword3), 
                                           output_dataset=[])        
        if data.input_dataset.conbined_keyword == None:
            return {"error": "少なくとも1つのキーワードを指定してください。"}
        urls = search_bot.get_search_urls_by_keyword(data.input_dataset.conbined_keyword, page_num)
        for (rank , url) in enumerate(urls):
            #rank(順位)とurlをセット, 
            search_result = SearchResult(rank=rank, 
                                         url=url, 
                                         summary=None) #summaryは後でセットする 
            text_content:str = parser.fetch_content_from_url(url)
            search_result.summary = response_getter.get_summary_by_prompt_content(const_prompt, text_content)
            #search_result.summary = text_content #MOCK
            
            #結果を格納
            data.output_dataset.append(search_result)
            rank += 1
        return {"API Succeeded" : True, "data" : data}
    
    except Exception as e:
            return {"API error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    #uvicorn main:app --host 0.0.0.0 --port 5000 --reload