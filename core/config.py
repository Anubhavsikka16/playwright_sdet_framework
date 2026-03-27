from dotenv import load_dotenv
import os

ENV= os.getenv('ENV', 'staging')  # default to 'staging' if ENV is not set and ENV Is not set here, so default is your env
print(f"Loading environment variables from env.{ENV}")
load_dotenv(f"env.{ENV}")

class Config:
    BASE_URL = os.getenv("BASE_URL")
    API_BASE_URL = os.getenv("API_BASE_URL")
    USERNAME = os.getenv("USERNAME")
    PASSWORD = os.getenv("PASSWORD")
    HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"
    BROWSER = os.getenv("BROWSER", "chromium").lower()

config = Config()