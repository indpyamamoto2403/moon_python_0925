import os, json
from pprint import pprint
from dotenv import load_dotenv
load_dotenv()

#utils
from utils import TextSplitter, Trimmer
from HTMLparser import HTMLParser
#repository
from OpenAIRespondRepository import OpenAIRespondRepository
from BingNewsRepository import BingNewsRepository
#DTO
from EntireDataset import EntireDataset
from KeywordInputDataset import InputDataset
from SummarizationDataset import SummarizationDataset
from SearchResult import SearchResult
from SplitInfo import SplitInfo
from Chunk import Chunk

class FetchNewsByKeywordService:
    def __init__(self, api_key, endpoint, search_api_key, search_endpoint):
        self.const_keyword = "ニュース"
        self.summary_prompt = "次のニュース原文を200字程度で要約してください。　"
        self.make_title_prompt = "次のニュース原文を読んで、30字程度でタイトルをつけてください。　"
        self.api_key = api_key
        self.endpoint = endpoint
        self.search_api_key = search_api_key
        self.search_endpoint = search_endpoint
        self.parser = HTMLParser()
        self.openai_repository = OpenAIRespondRepository(self.api_key, self.endpoint)
        self.bing_repository = BingNewsRepository(self.search_api_key, self.search_endpoint)
        self.trimmer = Trimmer()
        self.text_splitter = TextSplitter()
    
    def fetch(self, keyword1, keyword2="", keyword3="", search_num=5):
        """
        キーワードを受け取り、ニュースを返すエンドポイント
        """
        entire_dataset = EntireDataset(input_dataset=InputDataset(keyword1, keyword2, keyword3, self.const_keyword))
        combined_keyword = entire_dataset.input_dataset.get_combined_keyword()
        search_urls = self.bing_repository.fetch_urls_by_keyword(combined_keyword, search_num)
        
        for search_url in  search_urls:
            origin = self.parser.fetch_content_from_url(search_url)
            summary = self.openai_repository.fetch_answer(self.summary_prompt + origin)
            title = self.openai_repository.fetch_answer(self.make_title_prompt + summary)
            entire_dataset.output_dataset.append(SearchResult(url=search_url, 
                                                              origin=origin, 
                                                              summary=summary, 
                                                              title=title))        
        return entire_dataset

#テスト動作確認
if __name__ == "__main__":
    fetch_news = FetchNewsByKeywordService(
        api_key=os.getenv("API_KEY"),
        endpoint=os.getenv("ENDPOINT"),
        search_api_key=os.getenv("SUBSCRIPTION_KEY"),
        search_endpoint=os.getenv("SEARCH_ENDPOINT")
    )
    result = fetch_news.fetch("証券業務", "金融", "株価", 2)
    pprint(result)