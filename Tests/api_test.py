from fastapi.testclient import TestClient
from main import app  # Replace 'myapp' with the actual name of your FastAPI app module
client = TestClient(app)

#ルートディレクトリのテスト
def test_connect_to_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "AI FastAPI World"}

#質問エンドポイントのテスト
def test_question_endpoint():
    test_question = "What is the capital of France?"
    response = client.get(f"/question/{test_question}")
    assert response.status_code == 200
    print(response.json())

#Search URLのテストケース
def test_search_url_endpoint():
    test_keyword = "Python"
    response = client.get(f"/search_url/{test_keyword}")
    assert response.status_code == 200
    print(response.json())
    #URLが返されることを確認
    assert "https://www.python.org" in response.json()