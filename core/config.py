#All other files read settings from here instead of reading .env directly.
'''What it stores
BASE_URL
API_URL
USERNAME
PASSWORD
DB values
HEADLESS
'''

'''How it connects
pages/ uses BASE_URL
api/ uses API_URL
services/ uses credentials
core/db_client.py uses DB values
conftest.py uses HEADLESS and BASE_URL'''
from core.env_manager import EnvManager

env = EnvManager()

from dotenv import load_dotenv
import os

#Instead of reading os.getenv() everywhere, all tests and framework files read from Config.

class Config:
    BASE_URL = env.get("BASE_URL")
    API_BASE_URL = env.get("API_BASE_URL")

    USERNAME = env.get("USERNAME")
    PASSWORD = env.get("PASSWORD")

    HEADLESS = env.get("HEADLESS", "false").lower() == "true" #
    # DB_HOST = os.getenv("DB_HOST")
    # DB_USER = os.getenv("DB_USER")
    # DB_PASSWORD = os.getenv("DB_PASSWORD")
    # DB_NAME = os.getenv("DB_NAME")

# 🔥 FAIL FAST
assert Config.BASE_URL, "BASE_URL is missing!"
assert Config.API_BASE_URL, "API_BASE_URL is missing!"
 
   
    #DB CONFIG
    
config = Config()