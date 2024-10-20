import os 
from dotenv import load_dotenv
load_dotenv()

from BingNewsRepository import BingNewsRepository, MockBingNewsRepository
bing_news_repository_mock = MockBingNewsRepository()
def test_fetch_url_by_keyword():
    keyword = "Python"
    url = bing_news_repository_mock.fetch_url_by_keyword(keyword)
    assert url == "https://example.com/Python"
    
def test_fetch_urls_by_keyword():
    keyword = "Python"
    url_num = 4
    urls = bing_news_repository_mock.fetch_urls_by_keyword(keyword, url_num)
    assert urls == ["https://example.com/Python_0",
                    "https://example.com/Python_1", 
                    "https://example.com/Python_2",
                    "https://example.com/Python_3"]