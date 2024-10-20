import requests
import traceback
from dotenv import load_dotenv
import os 

load_dotenv()

class BingNewsRepository:
    def __init__(self, subscription_key: str, search_endpoint: str):
        self.subscription_key = subscription_key
        self.endpoint = search_endpoint
        self.headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    
    def _get_params(self, keyword: str):
        '''
        search APIに送信するパラメーターを取得する
        '''
        return {
            "q": keyword,
            "textDecorations": True,
            "textFormat": "HTML",
        }
    
    def fetch_url_by_keyword(self, keyword: str) -> str:
        """
        与えられたキーワードを元に、トップURLを返却する
        取得する件数は1件のみである
        """
        try:
            response = requests.get(self.endpoint, headers=self.headers, params=self._get_params(keyword))
            response.raise_for_status()
            search_results = response.json()
            if "webPages" in search_results and "value" in search_results["webPages"]:
                # トップURLのみを取得する
                top_result_url = search_results["webPages"]["value"][0]["url"]
                return top_result_url
            else:
                # 検索結果がない場合
                return "No results found"
        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            return f"InternalServerError: {str(e)}\nTraceback: {traceback_str}"

    def fetch_urls_by_keyword(self, keyword: str, url_num=3) -> list[str]:
        """
        与えられたキーワードを元に、トップURLを返却する
        取得する件数はurl_numである
        """
        try:
            response = requests.get(self.endpoint, headers=self.headers, params=self._get_params(keyword))
            response.raise_for_status()
            search_results = response.json()
            if "webPages" in search_results and "value" in search_results["webPages"]:
                # Assuming you want the first result's URL
                top_result_urls = []
                for i in range(url_num):
                    top_result_urls.append(search_results["webPages"]["value"][i]["url"])
                return top_result_urls
            else:
                return "No results found"
        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            return f"InternalServerError: {str(e)}\nTraceback: {traceback_str}"


class MockBingNewsRepository:
    def __init__(self):
        # 初期化は必要ないので、何もしません
        pass
    
    def fetch_url_by_keyword(self, keyword: str) -> str:
        """
        キーワードによってモックデータを返す
        """
        if keyword == "no_results":
            return "No results found"
        elif keyword == "error":
            return "InternalServerError: Simulated error"
        else:
            return f"https://example.com/{keyword}"
    
    def fetch_urls_by_keyword(self, keyword: str, url_num=3) -> list[str]:
        """
        キーワードとurl_numに基づいてモックデータを返す
        """
        if keyword == "no_results":
            return "No results found"
        elif keyword == "error":
            return "InternalServerError: Simulated error"
        else:
            # モックURLのリストを返す
            return [f"https://example.com/{keyword}_{i}" for i in range(url_num)]



if __name__ == "__main__":
    seach_page = BingNewsRepository(subscription_key = os.getenv('SUBSCRIPTION_KEY'), search_endpoint = os.getenv('SEARCH_ENDPOINT'))
    result_url = seach_page.fetch_url_by_keyword("VueJS")
    print(result_url)
    result_urls = seach_page.fetch_urls_by_keyword("Python", url_num=10)
    print(result_urls)