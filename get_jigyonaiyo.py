import requests
from env import * 
from html_parser import HTMLParser

class GetJigyonaiyo:
    def __init__(self, api_key:str, endpoint:str) -> None:
        self.api_key = api_key
        self.endpoint = endpoint
        self.parser = HTMLParser()
    
    def _question_answer(self, question:str) -> str:
        '''
        内部メソッド
        質問を受取、生成AIが処理し、結果を返す
        '''
        headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

        # Payload for the request
        payload = {
        "messages": [
            {
            "role": "system",
            "content": [
                {
                "type": "text",
                "text": question
                }
            ]
            }
        ],
        "temperature": 0.7,
        "top_p": 0.95,
        "max_tokens": 3000
        }


        # Send request
        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

        answer = response.json()["choices"][0]["message"]["content"]
        return answer
    

    def get_answer_by_url(self, url_path: str) -> str:
        '''
        URLとクエリを受取、生成AIが処理し、結果を返す
        '''
        question = "次の文章を参考に、事業内容を要約してください。"
        content = self.parser.fetch_content_from_url(url_path)
        prompt = question + content
        answer = self._question_answer(prompt)
        
        return {"url_path": url_path, "qestion": question, "answer": answer}


if __name__ == "__main__":
    jigyo = GetJigyonaiyo(API_KEY, ENDPOINT)
    print(jigyo.get_answer_by_url("https://www.jp-bank.japanpost.jp/kojin/sokin/furikomi/kouza/kj_sk_fm_kz_1.html"))