from Class.dataset import * 
from utils import TextSplitter
from get_prompt import GetPrompt
from openai import AzureOpenAI
from get_vector import EmbeddingProcessor
class ResponseGetter:
    '''
    promptとcontent, split_chunk_size, split_overlapを受け取り、
    contentを分割し、それぞれに対してpromptを実行し、統合プロンプトを返す関数を持つクラス
    '''
    def __init__(self, get_prompt:GetPrompt,split_chunk_size:int, split_overlap:int):
        '''
        promptのゲッターをコンストラクタで受け取る
        '''
        self.get_prompt = get_prompt
        self.split_chunk_size = split_chunk_size
        self.split_overlap = split_overlap
        
    def get_summary_by_prompt_content(self, arg_prompt:str, content:str):
        '''
        クエリ文字列としてプロンプトを受取、文章に分割し、それぞれに対してプロンプトを実行し、統合プロンプトを返す
        '''
        dataset = SummarizationDataset(prompt=arg_prompt, origin_text=content, split_info=SplitInfo(self.split_chunk_size, self.split_overlap))
        if len(content) > self.split_chunk_size:
            dataset.execute_split = True
            split_texts = TextSplitter.split(content, 
                                            chunk_size=self.split_chunk_size, 
                                            chunk_overlap=self.split_overlap)
            for index, chunk in enumerate(split_texts['chunks']):
                summary = self.get_prompt._question_answer(arg_prompt + chunk['text'])
                dataset.ChunkSet.append(Chunk(index=index, chunk=chunk['text'], summary=summary))            
            dataset.set_integration_content()
            dataset.summary = self.get_prompt._question_answer(arg_prompt + dataset.integration_content)
        else:
            #分割する必要がない場合は、文字列が返る
            dataset.execute_split = False
            dataset.summary = self.get_prompt._question_answer(arg_prompt + content)                
        return dataset

class RagResponseGetter(ResponseGetter):
    def __init__(self, 
                 get_prompt:GetPrompt, 
                 split_chunk_size:int, 
                 split_overlap:int, 
                 embedding_processor:EmbeddingProcessor):
        '''
        ResponseGetterの初期化に加えて、エンベディングモデルをインスタンス変数として保持する
        #引数の説明
        get_prompt: GetPrompt
        split_chunk_size: int
        split_overlap: int
        embedding_model: AzureOpenAI
        '''
        # 親クラス ResponseGetter の初期化
        super().__init__(get_prompt, split_chunk_size, split_overlap)
        self.embedding_processor = embedding_processor #AzureOpenAIのクライアントを初期化
    
    def get_summary_by_rag(self, arg_prompt:str, content:str):
        
        vector_query = self.embedding_processor.generate_embedding(arg_prompt)
        dataset = SummarizationDataset(prompt=arg_prompt, origin_text=content, split_info=SplitInfo(self.split_chunk_size, self.split_overlap))
        if len(content) > self.split_chunk_size:
            split_texts = TextSplitter.split(content, 
                                            chunk_size=self.split_chunk_size, 
                                            chunk_overlap=self.split_overlap)
            
            for index, chunk in enumerate(split_texts['chunks']):
                vector_chunk = self.embedding_processor.generate_embedding(chunk["text"])
                cosine_similarity = self.embedding_processor.cosine_similarity(vector_query, vector_chunk)
                dataset.ChunkSet.append(RaggedChunk(index=index, chunk=chunk['text'], cosine_similarity = cosine_similarity))
                #ChunkSetをcosine.simiralityでソート
                dataset.ChunkSet.sort(key=lambda x: x.cosine_similarity, reverse=True)

            dataset.integration_content = dataset.ChunkSet[0].chunk
            dataset.summary = self.get_prompt._question_answer(arg_prompt + dataset.integration_content)
        return dataset
