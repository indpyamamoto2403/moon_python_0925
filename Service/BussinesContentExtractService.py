import os 
from dotenv import load_dotenv
load_dotenv()

#utils
from utils import TextSplitter

#repository
from OpenAIRespondRepository import OpenAIRespondRepository
from BingNewsRepository import BingNewsRepository
from HTMLparser import HTMLParser

class BusinessContentExtractService:
    def __init__(self, api_key:str, endpoint:str, search_api_key:str, search_endpoint:str):
        self.repository = OpenAIRespondRepository(api_key, endpoint)
        self.news_repository = BingNewsRepository(search_api_key, search_endpoint)
        self.parser = HTMLParser()
    
    def get_business_content_by_url(self, url:str, arg_prompt:str)->str:
        '''
        URLを受取、本文を抽出、事業内容を要約して返す
        '''
        #URL本文
        content = self.parser.fetch_content_from_url(url)
        prompt = arg_prompt + content
        answer = self.repository.fetch_answer(prompt)
        return {"url": url, "content": content, "answer": answer}
    
    def get_business_content_by_keyword(self, keyword:str, prompt:str)->str:
        '''
        キーワードを受取、事業内容を抽出して返す
        '''
        #URL取得
        url = self.news_repository.fetch_url_by_keyword(keyword)
        content = self.parser.fetch_content_from_url(url)
        prompt = prompt + content
        answer = self.repository.fetch_answer(prompt)
        return {"keyword":keyword, "url": url, "content": content, "answer": answer}