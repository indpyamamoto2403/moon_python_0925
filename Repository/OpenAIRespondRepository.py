import os
import requests
from HTMLparser import HTMLParser
from utils import TextSplitter
from OpenAIRepositoryInterface import OpenAIRepositoryInterface

class OpenAIRespondRepository(OpenAIRepositoryInterface):
    def __init__(self, api_key:str, endpoint:str) -> None:
        self.api_key = api_key
        self.endpoint = endpoint
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