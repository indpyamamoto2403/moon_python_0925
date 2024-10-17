import os, json
from dotenv import load_dotenv
load_dotenv()

#utils
from utils import TextSplitter, Trimmer

#repository
from OpenAIRespondRepository import OpenAIRespondRepository

#DTO
from SummarizationDataset import SummarizationDataset
from SplitInfo import SplitInfo
from Chunk import Chunk

class GetClusterService:
    def __init__(self, api_key, endpoint):
        self.api_key = api_key
        self.endpoint = endpoint
        self.repository = OpenAIRespondRepository(self.api_key, self.endpoint)
        
        self.prompt =  """    
        #業種区分
        1.建設・不動産（総合建設業）
        2.建設・不動産（設備・内外装関連）
        3.建設・不動産（土木・造園）
        4.建設・不動産（建設設計業）
        5.建設・不動産（不動産業）
        6.建設・不動産（その他）
        7.製造（非鉄金属および金属製品）
        8.製造（ゴム・プラスチック・化学製品）
        9.製造（各種機械器具）
        10.製造（電気機器・電子部品・制御盤等）
        11.製造（金属）
        12.製造（紙製品）
        13.製造（印刷および印刷関連）
        14.製造（飲食料品）
        15.製造（医療・繊維・革・服飾雑貨品）
        16.製造（家具・雑貨・生活用品）
        17.製造（医薬・化粧品）
        18.製造（その他）
        19.商社・卸売（非鉄金属および金属製品）
        20.商社・卸売（ゴム・プラスチック・化学製品）
        21.商社・卸売（各種機械器具）
        22.商社・卸売（紙製品）
        23.商社・卸売（飲食料品）
        24.商社・卸売（医療・繊維・革・服飾雑貨品）
        25.商社・卸売（家具・雑貨・生活用品）
        26.商社・卸売（医薬・化粧品）
        27.商社・卸売（その他）
        28.情報・通信・広告（WEB制作）
        29.情報・通信・広告（IT・システム開発）
        30.情報・通信・広告（ソフトウェア・アプリケーション）
        31.情報・通信・広告（広告・映像等企画制作）
        32.情報・通信・広告（その他）
        33.専門・技術サービス（人材派遣・職業紹介）
        34.専門・技術サービス（運輸・倉庫）
        35.専門・技術サービス（警備・設備メンテナンス）
        36.専門・技術サービス（自動車整備）
        37.専門・技術サービス（廃棄物処理）
        38.専門・技術サービス（機械修理）
        39.専門・技術サービス（その他）
        40.コンサルティング（税務・会計）
        41.コンサルティング（法務・知的財産）
        42.コンサルティング（人事・労務）
        43.コンサルティング（その他）
        44.小売り（各種機械器具）
        45.小売り（飲食料品）
        46.小売り（医療・遷移・革・服飾雑貨品）
        47.小売り（家具・雑貨・生活用品）
        48.小売り（医薬・化粧品）
        49.小売り（その他）
        50.生活サービス（飲食）
        51.生活サービス（旅行・宿泊・娯楽）
        52.生活サービス（理美容・浴場）
        53.生活サービス（その他）
        54.医療・福祉・教育（医療）
        55.医療・福祉・教育（福祉・介護）
        56.医療・福祉・教育（教育・学習支援）
        57.医療・福祉・教育（その他）
        58.金融・保険（保険）
        59.金融・保険（その他）
        60.その他（上記に属さない事業）
        
        #要望
        次の文章を以下の分類に分けてください。
        cluster_id(int): 1~60
        foreign_interest(tinyint):0,1 外国に関心があるかどうか
        environmental_concern(bool):0,1 環境に関心があるかどうか
        
        #出力形式
        {
            {"cluster_id":""},
            {"foreign_interest:""},
            {environmental_concern:""}
        }
        
        #文章
        """

    def fetch_answer(self, sentence):
        '''
        入力されたsentenceを基に回答（JSON）を取得する
        '''
        
        try:
            # Parse the response to a Python dictionary
            response = self.repository.fetch_answer(self.prompt + sentence)
            cleaned_response = Trimmer.clean_json(response.strip())
            parsed_response = json.loads(cleaned_response)
            return parsed_response
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON response: {e}")
            return None
    
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
    cluster = GetClusterService(api_key = os.getenv("API_KEY"), endpoint = os.getenv("ENDPOINT"))
    print(cluster.fetch_answer("ボルトのねじなどを作成しています。"))
    