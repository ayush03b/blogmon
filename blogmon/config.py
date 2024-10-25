import os
from dotenv import load_dotenv
load_dotenv()
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'e11c832c6aff3df7c9f583eca450eab6')
    SQLALCHEMY_DATABASE_URI = os.getenv('SQLALCHEMY_DATABASE_URI', 'sqlite:///site.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv('SQLALCHEMY_TRACK_MODIFICATIONS', 'False')
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME', 'its2003ayush@gmail.com')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD', 'svjc vlzd pflv jrcx')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL') == 'True'
    FLASK_APP = os.getenv('FLASK_APP', 'blogmon')