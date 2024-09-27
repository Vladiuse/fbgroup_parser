from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from datetime import date
from lib_parser.src.types import AdsStatus

load_dotenv()



class Config(BaseSettings):
    NEW_URLS_FILE_PATH: str
    MAX_REQUEST_ERROR_ROW_COUNT: int
    START_DATE: date
    ADS_STATUS: AdsStatus


config = Config()