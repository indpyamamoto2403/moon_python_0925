from abc import ABC, abstractmethod

class BingNewsRepositoryInterface(ABC):
    @abstractmethod
    def fetch_url_by_keyword(self, query:str) -> str:
        pass
    
    def fetch_urls_by_keyword(self, query:str) -> str:
        pass