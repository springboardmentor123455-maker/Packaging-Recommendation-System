import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    uri = os.getenv("SQLALCHEMY_DATABASE_URI")

    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)

    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False