
from fastapi import FastAPI, Query, Path
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import uvicorn
import os 

#Repository
from OpenAIRespondRepository import OpenAIRespondRepository
from OpenAIImageRespondRepository import OpenAIImageRespondRepository
from BingNewsRepository import BingNewsRepository

#service
from BussinesContentExtractService import BusinessContentExtractService
from OpenAIRespondService import OpenAIRespondService
from OpenAIImageRespondService import OpenAIImageRespondService
from BingNewsService import BingNewsService
from GetClusterService import GetClusterService
from FetchNewsByKeywordService import FetchNewsByKeywordService

load_dotenv()

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)


#Repository
openai_respond_repository = OpenAIRespondRepository(api_key = os.getenv("API_KEY"), endpoint=os.getenv("ENDPOINT"))
openai_image_respond_repository = OpenAIImageRespondRepository(api_key = os.getenv("API_KEY"), endpoint=os.getenv("ENDPOINT"))
bing_news_repository = BingNewsRepository(subscription_key = os.getenv("SUBSCRIPTION_KEY"), search_endpoint=os.getenv("SEARCH_ENDPOINT"))

#service
business_extractor = BusinessContentExtractService(openai_respond_repository, bing_news_repository)
openai_responder = OpenAIRespondService(openai_respond_repository)
openai_image_responder = OpenAIImageRespondService(openai_image_respond_repository)
cluster = GetClusterService(openai_respond_repository)
bing_news = BingNewsService(bing_news_repository)
fetch_news = FetchNewsByKeywordService(openai_respond_repository, bing_news_repository)


@app.get("/")
def read_root():
    return {"Hello": "AI FastAPI World"}


@app.post("/question_answer_by_image")
def index(prompt: str, encoded_image: str):
    """
    これには、エンコードされた画像を受け取り、回答を返すエンドポイントが含まれます。
    """
    answer = openai_image_responder.fetch_answer(prompt, encoded_image)
    print(answer)
    return answer

@app.post("/url_query")
def index(url: str, prompt:str):
    """
    URLを受け取り、
    回答(事業内容の要約）を返すエンドポイントが含まれます。
    """
    answer = business_extractor.get_business_content_by_url(url, prompt)
    return answer

@app.get("/keyword_query")
def index(keyword: str, prompt:str):
    """
    クエリ文字列としてキーワードを受け取り,BingAPIで検索を行い
    得られた全文に対してpromptを作用させ、回答を返すエンドポイントが含まれます.
    """
    answer = business_extractor.get_business_content_by_keyword(keyword, prompt)
    return answer

@app.post("/get_cluster")
def index(sentence: str):
    """
    sentenceを基にクラスター情報をJSON形式で返すエンドポイント
    プロンプトはサービスクラス内に埋め込まれている。
    """
    answer = cluster.fetch_answer(sentence)
    return answer

@app.get("/fetch_news")
def index(keyword1:str, keyword2:str="", keyword3:str="",search_num:int = 3):
    """
    キーワードを受け取り、BingAPI経由でニュースを取得するエンドポイント
    keyword1, keyword2, keyword3: キーワード
    search_num: 検索数
    """
    answer = fetch_news.fetch(keyword1, keyword2, keyword3, search_num)
    print(answer)
    return answer


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
    #uvicorn main:app --host 0.0.0.0 --port 5000 --reload
    
    