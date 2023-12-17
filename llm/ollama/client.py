import json
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

def generate(model, prompt, system=None, template=None, options=None, callback=None):
    try:
        url = f"{OLLAMA_HOST}/api/generate"
        payload = {
            "model": model,
            "prompt": prompt,
            "system": system,
            "template": template,
            "options": options
        }
        payload = {k: v for k, v in payload.items() if v is not None}

        with requests.post(url, json=payload, stream=True) as response:
            response.raise_for_status()
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    callback(chunk)
    except Exception as completion_exception:
        print(f"Failed to generate chat completion: {completion_exception}")