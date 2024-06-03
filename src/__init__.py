from flask import Flask
import os
from src.config.config import Config
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

app = Flask(__name__)

config = Config().dev_config

app.env = config.ENV

# connecting to mongodb
mongo_client = MongoClient(os.getenv("MONGO_URI"))
db = mongo_client["being"]

# import api blueprint to register it with app
from src.routes import api
app.register_blueprint(api, url_prefix = "/api")
