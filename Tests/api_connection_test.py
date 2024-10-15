import os 
from dotenv import load_dotenv
load_dotenv()
import requests
import pytest
from langchain.text_splitter import RecursiveCharacterTextSplitter

@pytest.fixture(scope="module")
def api_config():
    '''
    APIキーやエンドポイントなど、テスト全体で共通の設定をまとめるフィクスチャ
    '''
    return {
        "api_key": os.getenv("API_KEY"),
        "endpoint": os.getenv("ENDPOINT"),
        "subscription_key": os.getenv("SUBSCRIPTION_KEY"),
        "search_endpoint": os.getenv("SEARCH_ENDPOINT"),
    }


def test_addition():
    '''
    pytestが走るかどうかのテスト
    '''
    assert 1 + 1 == 2
    
def test_openai_api_connection(api_config):
    '''
    OpenAI APIとの接続テスト
    '''
    headers = {
        "Content-Type": "application/json",
        "api-key": api_config["api_key"],
    }
        
    payload = {
        "messages": [
        {
            "role": "system",
            "content": [
            {
                "type": "text",
                "text": "hi, how are you?"
            }
            ]
        }
        ],
        "temperature": 0.1,
        "top_p": 0.95,
        "max_tokens": 3000
    }
    response = requests.post(api_config["endpoint"], headers=headers, json=payload)
    assert response.status_code == 200
    
    
def test_bing_news_api_connection(api_config):
    '''
    Bing News APIとの接続テスト
    '''
    headers = {"Ocp-Apim-Subscription-Key": api_config["subscription_key"]}
    params = {
        "q": "Apple",
        "textDecorations": True,
        "textFormat": "HTML",
    }
    response = requests.get(api_config["search_endpoint"], headers=headers, params=params)
    assert response.status_code == 200

    
def test_text_split():
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=30,
        chunk_overlap=0
    )
    
    long_text = "ここに長い文章が入ります" * 10
    split_texts = text_splitter.split_text(long_text)
    assert len(split_texts) == 4