import os, json
from dotenv import load_dotenv
load_dotenv()

#utils
from utils import TextSplitter, Trimmer
from HTMLparser import HTMLParser
#repository
from OpenAIRespondRepository import OpenAIRespondRepository
from BingNewsRepository import BingNewsRepository
#DTO
from SummarizationDataset import SummarizationDataset
from SplitInfo import SplitInfo
from Chunk import Chunk

class FetchNewsByKeywordService:
    def __init__(self):
        self.const_keyword = "ニュース"
        self.api_key = os.getenv("API_KEY")
        self.endpoint = os.getenv("ENDPOINT")
        self.search_api_key = os.getenv("SUBSCRIPTION_KEY")
        self.search_endpoint = os.getenv("SEARCH_ENDPOINT")
        self.parser = HTMLParser()
        self.openai_repository = OpenAIRespondRepository(self.api_key, self.endpoint)
        self.bing_repository = BingNewsRepository(self.search_api_key, self.search_endpoint)
        self.trimmer = Trimmer()
        self.text_splitter = TextSplitter()
    
    def fetch(self, keyword1, keyword2="", keyword3="", search_num=5):
        """
        キーワードを受け取り、ニュースを返すエンドポイント
        """
        search_keyword = keyword1 + " " + keyword2 + " " + keyword3 + " " + self.const_keyword
        search_urls = self.bing_repository.fetch_urls_by_keyword(search_keyword, search_num)
        
        for search_url in  search_urls:
            origin = self.parser.fetch_content_from_url(search_url)
            prompt = "次の原文を200字程度で要約してください。　"
            summary = self.openai_repository.fetch_answer(prompt + origin)
            print(summary)
        
    

if __name__ == "__main__":
    fetch_news = FetchNewsByKeywordService()
    result = fetch_news.fetch("証券業務", "金融", "株価")