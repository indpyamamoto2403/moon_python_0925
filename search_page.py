import requests
import traceback

class SearchPage:
    def __init__(self, subscription_key: str, search_endpoint: str):
        
        self.subscription_key = subscription_key
        self.endpoint = search_endpoint
        self.headers = {"Ocp-Apim-Subscription-Key": subscription_key}
        

    
    def _get_params(self, keyword: str):
        '''
        search APIに送信するパラメーターを取得する
        '''
        return {"q": keyword}
    
    def get_search_url_by_keyword(self, keyword: str):
        """
        与えられたキーワードを元に、トップURLを返却する
        """
        try:
            response = requests.get(self.endpoint, headers=self.headers, params=self._get_params(keyword))
            response.raise_for_status()
            search_results = response.json()
            # Extract the first URL from the search results
            if "webPages" in search_results and "value" in search_results["webPages"]:
                # Assuming you want the first result's URL
                top_result_url = search_results["webPages"]["value"][0]["url"]
                return top_result_url
            else:
                return "No results found"
        except Exception as e:
            traceback_str = ''.join(traceback.format_tb(e.__traceback__))
            return f"InternalServerError: {str(e)}\nTraceback: {traceback_str}"
    
#テスト
if __name__ == "__main__":
    from env import * # 環境変数を読み込む
    seach_page = SearchPage(subscription_key = SUBSCRIPTION_KEY, search_endpoint = SEARCH_ENDPOINT)
    result_url = seach_page.get_search_url_by_keyword("VueJS")
    print(result_url)