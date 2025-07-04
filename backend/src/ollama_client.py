import requests

class OllamaClient:
    def __init__(self, host="http://localhost:11434"):
        self.base_url = host

    def generate(self, prompt, model="llama3.2"):
        resp = requests.post(f"{self.base_url}/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        return resp.json() 

    def chat(self, messages, model="llama3.2"):
        resp = requests.post(f"{self.base_url}/api/chat", json={
            "model": model,
            "messages": messages,
            "stream": False
        })
        return resp.json() 
