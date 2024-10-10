import requests
import json
import base64
from html_parser import HTMLParser
from utils import TextSplitter

class GetPrompt:
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
            "temperature": 0.7,
            "top_p": 0.95,
            "max_tokens": 2000
        }
    
    def _question_answer(self, question:str) -> str:
        '''
        内部メソッド
        質問を受取、生成AIが処理し、結果を返す
        '''
        try:
            response = requests.post(self.endpoint, headers=self.headers, json=self.payload(question))
            response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code
        except requests.RequestException as e:
            raise SystemExit(f"Failed to make the request. Error: {e}")

        answer = response.json()["choices"][0]["message"]["content"]
        return answer
    
    def _question_answer_by_split(self, prompt: str, content: str) -> dict:
        '''
        クエリ文字列としてプロンプトを受取、文章に分割し、それぞれに対してプロンプトを実行し、統合プロンプトを返す
        '''
        result = {"partials": []}  # Initialize result as a dictionary
        split_chunk_size = 1000
        split_overlap = 20

        if len(content) > split_chunk_size:
            split_texts = TextSplitter.split(content, 
                                            chunk_size=split_chunk_size, 
                                            chunk_overlap=split_overlap)
            for chunk in split_texts['chunks']:
                partial_result = self._question_answer(prompt + chunk['text'])
                result["partials"].append(partial_result)
        else:
            partial_result = self._question_answer(prompt + content)
            result["partials"].append(partial_result) 
        result["summary"] = ' '.join(result["partials"])

        return result

    
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

    def summarize_news(self, content:str) -> str:
        '''
        テキストを受取、要約を返す
        '''
        prefix = "次の文章のニュース記事を要約してください。"
        prompt = prefix + content
        answer = self._question_answer(prompt)
        
        return {"prefix": prefix, "summary": answer}
    