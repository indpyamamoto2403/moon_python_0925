import requests
import os
import base64
from HTMLparser import HTMLParser
from utils import TextSplitter
from dotenv import load_dotenv
load_dotenv()
from OpenAIRepositoryInterface import OpenAIRepositoryInterface

class OpenAIImageRespondRepository(OpenAIRepositoryInterface):
    def __init__(self, api_key: str, endpoint: str) -> None:
        self.api_key = api_key
        self.endpoint = endpoint
        self.parser = HTMLParser()
        self.headers = {
            "Content-Type": "application/json",
            "api-key": self.api_key,
        }

    def fetch_answer(self, prompt:str, encoded_image: str) -> str:
        '''
        Internal method to process a question and get an answer using AI for the provided image.
        '''
        payload = {
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpg;base64,{encoded_image}"
                            },
                        },
                    ]
                }
            ],
            "temperature": 0.1,
            "top_p": 0.95,
            "max_tokens": 3000
        }

        try:
            response = requests.post(self.endpoint, headers=self.headers, json=payload)
            response.raise_for_status()
        except requests.RequestException as e:
            print(f"Failed to make the request. Error: {e}")
            return "Error in fetching the answer."
        
        answer = response.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        return answer

if __name__ == "__main__":
    image_responder = OpenAIImageRespondRepository(api_key=os.getenv("API_KEY"), endpoint=os.getenv("ENDPOINT"))
    
    #同階層のsample.jpgをbase64エンコード
    with open("sample2.png", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    answer = image_responder.fetch_answer(encoded_image)