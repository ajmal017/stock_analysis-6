from flask import Flask
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
#imports class Config from ../config.py

from app import routes
