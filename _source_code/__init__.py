from flask import Flask
from models import db

app = Flask(__name__)

# config
app.secret_key = 'development key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/test.db'

db.init_app(app)


# import routes
import routes