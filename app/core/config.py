import os

from dotenv import load_dotenv


class Settings:
     load_dotenv()
     
     alg = os.environ.get('ALG')
     secret = os.environ.get('SECRET')
     url = os.environ.get('URL')
     
     
settings = Settings()
