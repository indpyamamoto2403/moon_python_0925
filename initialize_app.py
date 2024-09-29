from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def initialize_app(app : FastAPI) ->None:
    app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allow all headers
)