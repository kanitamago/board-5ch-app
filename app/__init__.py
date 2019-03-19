from flask import Flask
from flask_sqlalchemy import SQLAlchemy

#アプリ生成
app = Flask(__name__)
app.config.from_object("app.config")

db = SQLAlchemy(app)

from app.views import views
