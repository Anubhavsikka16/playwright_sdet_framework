import os
from dotenv import load_dotenv
#“This file is responsible for loading environment-specific configuration dynamically, so the framework is environment-aware.”
class EnvManager:

    def __init__(self):
        env = os.getenv("ENV", "prod") #--> default to prod if ENV is not set, but you can set it to staging or any other env you have

        # 🔥 build correct path to .env file
        
        load_dotenv(f".env.{env}")

    def get(self, key, default=None):
        return os.getenv(key, default)