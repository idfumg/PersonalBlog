from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.oidc import OpenIDConnect

app = Flask(__name__)
app.config.from_object('config')

db = SQLAlchemy(app)

oidc = OpenIDConnect(app, {})

from app import views, models
