import requests

class BingNewsAPIRepository:
    def __init__(self, api_key, endpoint="https://api.bing.microsoft.com/v7.0/news/search"):
        self.api_key = api_key
        self.endpoint = endpoint
    
    def get_news(self, query):
        try:
            response = requests.get(
                f'{self.endpoint}?q={query}',
                headers={'Ocp-Apim-Subscription-Key': self.api_key}
            )
            response.raise_for_status()  # Check if the request was successful
            return response.json()  # Return the JSON response
        except requests.exceptions.RequestException as e:
            print(f"Error fetching news: {e}")
            return None

# Test code
if __name__ == "__main__":
    # Replace 'your_api_key' with your actual Bing News API key
    api_key = 'c3c1c5ef17d44b199e24af40f2338bb7'
    query = 'technology'
    
    bing_news = BingNewsAPIRepository(api_key)
    
    # Fetch and print the news articles
    news_data = bing_news.get_news(query)
    if news_data:
        for article in news_data.get('value', []):  # Extract the articles list from the response
            print(f"Title: {article.get('name')}")
            print(f"URL: {article.get('url')}")
            print(f"Description: {article.get('description')}\n")
    else:
        print("No news articles found.")
