import requests
from bs4 import BeautifulSoup
from utils import Trimmer

class HTMLParser:
    '''
    htmlを解析するクラス
    '''
    def fetch_content_from_url(self, url):
        '''
        URLからHTMLを取得し、テキストを抽出して返す
        '''
        try:
            response = requests.get(url)
            response.raise_for_status()  # Raise an exception for HTTP errors
        except requests.exceptions.HTTPError as e:
            if response.status_code == 404:
                return "404:ページが見つかりませんでした"
            else:
                raise e

        soup = BeautifulSoup(response.text, 'html.parser')
        text_content = soup.get_text()
        text_content = Trimmer.trim_spaces(text_content)
        return text_content

if __name__ == "__main__":
    #使用例
    parser = HTMLParser()
    text_content = parser.fetch_content_from_url('https://www.asahi.com/and/pressrelease/425142064/')
    print(text_content)
