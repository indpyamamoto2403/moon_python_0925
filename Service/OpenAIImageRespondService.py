import os
from dotenv import load_dotenv
from utils import Trimmer
load_dotenv()

#Repository
from OpenAIImageRespondRepository import OpenAIImageRespondRepository

class OpenAIImageRespondService:
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint
        self.image_responder = OpenAIImageRespondRepository(api_key=self.api_key, endpoint=self.endpoint)
        
    def fetch_answer(self, prompt:str, encoded_image: str) -> str:
        '''
        Internal method to process a question and get an answer using AI for the provided image.
        '''
        answer = self.image_responder.fetch_answer(prompt, encoded_image)
        #JSON形式に整形
        trimmed_answer = Trimmer.clean_json(answer)
        return trimmed_answer
    

if __name__ == "__main__":
    image_responder = OpenAIImageRespondService(api_key=os.getenv("API_KEY"), endpoint=os.getenv("ENDPOINT"))
    from sample_encoded_image import sample_encoded_image
    print(image_responder.fetch_answer("What is this?", sample_encoded_image))
    #This is a business card from Meiji University in Japan