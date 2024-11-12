import os

class Config:

    SQLALCHEMY_DATABASE_URI = os.getenv(
    'choose your db url here'
)

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', "choose a secrect key")

