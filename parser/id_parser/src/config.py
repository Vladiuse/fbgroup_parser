from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()



class Config(BaseSettings):
    NEW_URLS_FILE_PATH: str

config = Config()