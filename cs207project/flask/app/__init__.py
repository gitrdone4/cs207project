from flask import Flask
from flask_api import FlaskAPI
from flask_sqlalchemy import SQLAlchemy

app = FlaskAPI(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models
