import pytest
import requests
from bs4 import BeautifulSoup
from unittest.mock import patch, MagicMock
from html_parser import HTMLParser
from utils import TextSplitter
from pprint import pprint
def test_html_parse():
    '''
    Test the HTMLParser class
    '''
    parser = HTMLParser()
    result = parser.fetch_content_from_url('https://www.python.org/')
    print(result)
    assert 'Python' in result
    
def test_text_split():
    long_text = "ここに長いテキストを挿入します。非常に長いテキストを想定しています。"
    result = TextSplitter.split(long_text, chunk_size=5, chunk_overlap=2)
    pprint(result)
    assert len(result['chunks']) == 11