import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY_FLASK_APP')
db = SQLAlchemy(app)
migrate = Migrate(app, db, render_as_batch=True)

from . import models, views, forms, api_views, error_handlers
