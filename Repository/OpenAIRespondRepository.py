import os
import requests
from HTMLparser import HTMLParser
from utils import TextSplitter
class OpenAIResponderRepository:
    
    def __init__(self, api_key:str, endpoint:str) -> None:
        self.api_key = api_key
        self.endpoint = endpoint
        self.parser = HTMLParser()
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }
        
        self.payload = lambda question: {
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
            "temperature": 0.1,
            "top_p": 0.95,
            "max_tokens": 3000
        }
    
    def fetch_answer(self, prompt:str) -> str:
        '''
        openAIのAPIキーを用いて、質問を受け取り、回答を返す
        '''
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=self.payload(prompt))
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

        answer = response.json()["choices"][0]["message"]["content"]
        return answer
    
    def fetch_answer_by_split(self, prompt: str, content: str) -> dict:
        '''
        クエリ文字列としてプロンプトを受取、文章に分割し、それぞれに対してプロンプトを実行し、統合プロンプトを返す
        '''
        answer = {"partials": []}  # Initialize result as a dictionary
        split_chunk_size = 1000
        split_overlap = 20

        if len(content) > split_chunk_size:
            split_texts = TextSplitter.split(content, 
                                            chunk_size=split_chunk_size, 
                                            chunk_overlap=split_overlap)
            for chunk in split_texts['chunks']:
                partial_result = self.fetch_answer(prompt + chunk['text'])
                answer["partials"].append(partial_result)
        else:
            partial_result = self.fetch_answer(prompt + content)
            answer["partials"].append(partial_result) 
        answer["summary"] = ' '.join(answer["partials"])
        return answer
