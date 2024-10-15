import os 
from dotenv import load_dotenv
from pprint import pprint
load_dotenv()

#utils
from utils import TextSplitter

#repository
from OpenAIRespondRepository import OpenAIRespondRepository

#DTO
from SummarizationDataset import SummarizationDataset
from SplitInfo import SplitInfo
from Chunk import Chunk

class OpenAIRespondService:
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint
        self.repository = OpenAIRespondRepository(self.api_key, self.endpoint)

    def fetch_answer(self, prompt):
        response = self.repository.fetch_answer(prompt)
        return response
    
    
    #分割処理にて回答を取得
    def fetch_answer_by_split(self, prompt, content):
        
        #チャンクサイズに関する設定
        chunk_size = 3000
        overlap = 0 
        split_info:SplitInfo = SplitInfo(chunk_size, overlap)
        
        #データセットの作成
        dataset = SummarizationDataset(prompt=prompt, origin_text=content, split_info=split_info)
        
        #コンテントがチャンクサイズより大きい場合、分割して処理
        if dataset.origin_text_length > chunk_size:
            split_texts:list[str] = TextSplitter.split(dataset.origin_text, 
                                             chunk_size=chunk_size, 
                                             chunk_overlap=overlap)
            for (index,chunk) in enumerate(split_texts['chunks']):
                partial_result = self.fetch_answer(prompt + chunk['text'])
                dataset.ChunkSet.append(Chunk(chunk = chunk, index = index, summary=partial_result))

            dataset.set_integration_content()
            dataset.summary = self.fetch_answer(prompt + dataset.integration_content)
        
        #コンテントがチャンクサイズより小さい場合、そのまま処理
        else:
            partial_result = self.fetch_answer(prompt + content)
            dataset.summary = partial_result
            
            
        return dataset

if __name__ == "__main__":
    openai_responder = OpenAIRespondService(api_key = os.getenv("API_KEY"), endpoint = os.getenv("ENDPOINT"))
    pprint(openai_responder.fetch_answer_by_split("What is the capital of Japan?", "Tokyo is the capital of Japan. Paris is the capital of France. London is the capital of England."))
    