from dotenv import load_dotenv
load_dotenv()

#repository
from OpenAIRepositoryInterface import OpenAIRepositoryInterface
from BingNewsRepositoryInterface import BingNewsRepositoryInterface

from OpenAIRespondRepository import OpenAIRespondRepository
from BingNewsRepository import BingNewsRepository
from HTMLparser import HTMLParser


#dto
from BusinessExtractionData import BusinessExtractionData

class BusinessContentExtractService:
    def __init__(self, openai_repository:OpenAIRepositoryInterface , news_repository:BingNewsRepositoryInterface):
        self.openai_repository = openai_repository
        self.news_repository = news_repository
        self.parser = HTMLParser()
    
    def get_business_content_by_url(self, url:str, arg_prompt:str)->str:
        '''
        URLを受取、本文を抽出、事業内容を要約して返す
        '''
        #URL本文
        data : BusinessExtractionData = BusinessExtractionData(search_type="url", 
                                                               keyword=None, 
                                                               url=url, 
                                                               prompt=arg_prompt)
        data.content = self.parser.fetch_content_from_url(url)
        question = data.prompt + data.content
        data.answer = self.openai_repository.fetch_answer(question)
        return data
        
    
    def get_business_content_by_keyword(self, keyword:str, prompt:str)->str:
        '''
        キーワードを受取、事業内容を抽出して返す
        '''
        #URL取得
        data : BusinessExtractionData = BusinessExtractionData(search_type="keyword", 
                                                               keyword=keyword, 
                                                               url=None, 
                                                               prompt=prompt)
        data.url = self.news_repository.fetch_url_by_keyword(keyword)
        data.content = self.parser.fetch_content_from_url(data.url)
        question = data.prompt + data.content
        data.answer = self.openai_repository.fetch_answer(question)
        return data