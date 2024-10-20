from BingNewsRepository import BingNewsRepository
from BingNewsRepositoryInterface import BingNewsRepositoryInterface

class BingNewsService:
    def __init__(self, bing_repository: BingNewsRepositoryInterface):
        self.bing_repository:BingNewsRepositoryInterface = bing_repository
        
    def fetch_url_by_keyword(self, keyword: str) -> str:
        """
        与えられたキーワードを元に、トップURLを返却する
        取得する件数は1件のみである
        """
        return self.bing_repository.fetch_url_by_keyword(keyword)
    
    def fetch_urls_by_keyword(self, keyword: str, url_num=3) -> list[str]:
        """
        与えられたキーワードを元に、トップURLを返却する
        取得する件数はurl_numである
        """
        return self.bing_repository.fetch_urls_by_keyword(keyword, url_num)