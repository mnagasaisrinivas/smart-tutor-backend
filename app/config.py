import os
from dotenv import load_dotenv
from datetime import timedelta


load_dotenv()

class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(days=1)      # 1 day
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)    # 30 days
    JWT_TOKEN_LOCATION = ["headers", "cookies"]
    JWT_COOKIE_SECURE = False  # Set to True in production with HTTPS
    JWT_COOKIE_HTTPONLY = True
    JWT_REFRESH_COOKIE_PATH = "/api/auth/refresh"
    JWT_ACCESS_COOKIE_PATH = "/"


