import requests
from core.config import config

class BaseClient:
    
    def __init__(self, base_url=None, headers=None):
        self.base_url = base_url or config.API_BASE_URL
        self.sessions=requests.Session()
        self.sessions.headers.update(headers or {"Content-Type": "application/json"})
        
    def get(self, path, **kwargs):
        return self.session.get(f"{self.base_url}{path}", **kwargs)# **kwargs: It allows you to pass any number of named arguments (key=value pairs) into a function.

    
    def post(self, path, **kwargs):
        return self.session.post(f"{self.base_url}{path}", **kwargs)

    def put(self, path, **kwargs):
        return self.session.put(f"{self.base_url}{path}", **kwargs)

    def delete(self, path, **kwargs):
        return self.session.delete(f"{self.base_url}{path}", **kwargs)