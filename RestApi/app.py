from flask import Flask
from sqlalchemy import create_engine
import os

engine = create_engine(os.getenv('DATABASE_CONNECT'))
engine.connect()

app = Flask(__name__)