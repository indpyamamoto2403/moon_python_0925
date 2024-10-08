import os
from fastapi import FastAPI, Query, Path
from get_prompt import GetPrompt
from search_page import SearchPage
from html_parser import HTMLParser
from utils import TextSplitter
from fastapi.middleware.cors import CORSMiddleware
import requests
from dotenv import load_dotenv
import uvicorn

from URLQuery import URLQuery
from dataset import NewsSearchResult, SearchResult, SummarizationDataset, Chunk, SplitInfo


load_dotenv()
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

split_chunk_size = 20
split_overlap = 0


@app.get("/")
def read_root():
    return {"Hello": "AI FastAPI World"}

@app.get("/question/{question}")
def index(question: str):
    """
    これには、質問を受け取り、回答を返すエンドポイントが含まれます。
    """
    answer = prompt._question_answer(question)
    return (question, answer)

@app.get("/question_answer_by_split")
def index(arg_prompt: str, content: str):
    '''
    クエリ文字列としてプロンプトを受取、文章に分割し、それぞれに対してプロンプトを実行し、統合プロンプトを返す
    '''
    if len(content) > split_chunk_size:
        dataset = SummarizationDataset(prompt=arg_prompt, origin_text=content, split_info=SplitInfo(split_chunk_size, split_overlap))
        split_texts = TextSplitter.split(content, 
                                         chunk_size=split_chunk_size, 
                                         chunk_overlap=split_overlap)
        for index, chunk in enumerate(split_texts['chunks']):
            summary = prompt._question_answer(arg_prompt + chunk['text'])
            dataset.ChunkSet.append(Chunk(index=index, chunk=chunk['text'], summary=summary))
        
        #統合コンテンツをセット
        dataset.set_integration_content()
        dataset.integration_summary = prompt._question_answer(arg_prompt + dataset.integration_content)
    else:
        #分割する必要がない場合は、文字列が返る
         dataset = prompt._question_answer(arg_prompt + content)
                
    return dataset

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
    これにはキーワードを受け取り、回答を返すエンドポイントが含まれます.
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

@app.get("/vector_search/{keyword}")
def index(keyword):
    answer = "ここにベクトル検索の結果が入ります。"
    return answer

@app.get("/news")
def index(page : int = Query(3), keyword1: str = Query(None),  keyword2: str = Query(None),keyword3: str = Query(None)):
    
    const_prompt = "次のニュース記事を要約してください"
    
    try:
        combined_keywords = f"{keyword1 or ''} {keyword2 or ''} {keyword3 or ''} ニュース".strip()
        if not combined_keywords:
            return {"error": "少なくとも1つのキーワードを指定してください。"}
        urls = search_bot.get_search_urls_by_keyword(combined_keywords, page)
        contents = []
        rank = 1
        for url in urls:
            content = {}
            text_content = parser.fetch_content_from_url(url)
            search_results = prompt.summarize_news(text_content)
            # 辞書に各項目を追加
            content['rank'] = rank
            content['url'] = url
            content['text_content'] = text_content
            content['search_results'] = search_results    
            rank += 1
            contents.append(content)
        return {"keywords": [keyword1, keyword2, keyword3], "url": urls, "news": contents}
    except Exception as e:
            return {"API error": str(e)}

@app.get("/news_search")
def index(page : int = Query(3), keyword1: str = Query(None),  keyword2: str = Query(None),keyword3: str = Query(None)):
    
    const_prompt = "次のニュース記事を要約してください"
    
    try:
        news : NewsSearchResult = NewsSearchResult(keyword1=keyword1, keyword2=keyword2, keyword3=keyword3, search_num=page, search_result=[])
        if not news.get_search_result():
            return {"error": "少なくとも1つのキーワードを指定してください。"}
        urls = search_bot.get_search_urls_by_keyword(news.search_word, page)
        

        for (rank , url) in enumerate(urls):
            
            #rank(順位)とurlをセット, 
            search_result = SearchResult(rank=rank, 
                                         url=url, 
                                         summary=None) #summaryは後でセットする
            
            text_content = parser.fetch_content_from_url(url)
            search_results = prompt.summarize_news(text_content)
            # 辞書に各項目を追加
            summary_dataset = SummarizationDataset(prompt=const_prompt, origin_text=text_content, split_info=SplitInfo(split_chunk_size, split_overlap))
            content['text_content'] = text_content
            content['search_results'] = search_results    
            rank += 1
            contents.append(content)
        return {"keywords": [keyword1, keyword2, keyword3], "url": urls, "news": contents}
    except Exception as e:
            return {"API error": str(e)}
    
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)