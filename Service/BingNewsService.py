from BingNewsRepository import BingNewsRepository

class BingNewsService:
    def __init__(self, subscription_key: str, search_endpoint: str):
        self.bing_news = BingNewsRepository(subscription_key = subscription_key, search_endpoint = search_endpoint)
        
    def fetch_url_by_keyword(self, keyword: str) -> str:
        """
        与えられたキーワードを元に、トップURLを返却する
        取得する件数は1件のみである
        """
        return self.bing_news.fetch_url_by_keyword(keyword)
    
    def fetch_urls_by_keyword(self, keyword: str, url_num=3) -> list[str]:
        """
        与えられたキーワードを元に、トップURLを返却する
        取得する件数はurl_numである
        """
        return self.bing_news.fetch_urls_by_keyword(keyword, url_num)