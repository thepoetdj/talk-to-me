import os
import requests

OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")

def models():
    no_models = []
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags")
        response.raise_for_status()
        data = response.json()
        return data.get("models", no_models)
    except requests.exceptions.RequestException as request_exception:
        print(f"Failed to fetch models: {request_exception}")
        return no_models
    
def show(name):
    try:
        url = f"{OLLAMA_HOST}/api/show"
        payload = {'name': name}
        response = requests.post(url=url, json=payload)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as request_exception:
        print(f"Failed to fetch model details for {name}: {request_exception}")
        return None
