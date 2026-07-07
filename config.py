import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'snack_vendor_secret'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt_snack_secret_key_long_enough_32chars'
