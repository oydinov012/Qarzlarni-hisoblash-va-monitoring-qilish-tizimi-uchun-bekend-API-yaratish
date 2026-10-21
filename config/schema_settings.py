import os

from dotenv import load_dotenv
load_dotenv()
from pydantic import BaseModel

class Settings(BaseModel):
    authjwt_secret_key : str = os.environ["AUTH_JWT_token"]
