from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object('cs207project.flask.config')
db = SQLAlchemy(app)

from cs207project.flask.app import views, models
