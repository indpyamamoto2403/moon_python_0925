import requests
import json
import base64
from html_parser import HTMLParser

class GetPrompt:
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
        "max_tokens": 2000
        }


        # Send request
        try:
            response = requests.post(self.endpoint, headers=headers, json=payload)
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

        answer = response.json()["choices"][0]["message"]["content"]
        return answer
    
    def _split_text(self, text:str) -> list:
        '''
        テキストを受取、文に分割してリストで返す
        '''
        return ["sentence1", "sentence2", "sentence3", "sentence4", "sentence5"]
    
    def get_answer_by_url(self, url_path: str) -> str:
        '''
        URLとクエリを受取、生成AIが処理し、結果を返す
        '''
        question = "次の文章を参考に、事業内容を要約してください。"
        content = self.parser.fetch_content_from_url(url_path)
        prompt = question + content
        answer = self._question_answer(prompt)
        
        return {"url_path": url_path, "qestion": question, "answer": answer}

    def get_answer_by_keyword(self, keyword: str) -> str:
        '''
        キーワードとクエリを受取、生成AIが処理し、結果を返す
        '''
        
        question = "次のキーワードについて、事業内容を教えてください。"
        prompt = question + keyword
        answer = self._question_answer(prompt)
        
        return {"keyword": keyword, "question": question, "answer": answer}
    
    
    def summarize_content(self, content:str) -> str:
        '''
        テキストを受取、要約を返す
        '''
        prompt = "次の文章を参考に、事業内容を要約してください。" + content
        answer = self._question_answer(prompt)
        
        return {"prompt": prompt, "summary": answer}