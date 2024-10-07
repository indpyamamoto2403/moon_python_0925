from pydantic import BaseModel

class URLQuery(BaseModel):
    url_path: str