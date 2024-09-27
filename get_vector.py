import os
from env import * 
from openai import AzureOpenAI
import numpy as np

# Azure OpenAIのクライアントを初期化
client = AzureOpenAI(
    api_key=EMBEDDING_API_KEY,  
    api_version="2024-06-01",
    azure_endpoint=EMBEDDING_ENDPOINT, 
)

# 埋め込みを生成する関数
def generate_embedding(input_text, model="text-embedding-3-small"):
    response = client.embeddings.create(
        input=input_text,
        model=model
    )
    return response.data[0].embedding

# コサイン類似度を計算する関数
def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    dot_product = np.dot(vec1, vec2)
    norm_vec1 = np.linalg.norm(vec1)
    norm_vec2 = np.linalg.norm(vec2)
    return dot_product / (norm_vec1 * norm_vec2)

# メイン処理
if __name__ == "__main__":
    # 埋め込みの取得
    content_embedding = generate_embedding("私の名前はブラックコーヒーです")
    query_embedding = generate_embedding("あなたの名前はブラックコーヒーですか？")
    no_correlation_embedding = generate_embedding("今日はいい天気ですね!")

    # コサイン類似度を計算
    similarity_1 = cosine_similarity(content_embedding, query_embedding)
    simirality_2 = cosine_similarity(content_embedding, no_correlation_embedding)
    simirality_3 = cosine_similarity(query_embedding, no_correlation_embedding)

    # 結果の表示
    print(f"コサイン類似度: {similarity_1:.4f}")
    print(f"コサイン類似度: {simirality_2:.4f}")
    print(f"コサイン類似度: {simirality_3:.4f}")
