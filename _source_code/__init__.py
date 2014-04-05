from flask import Flask
from models import db

app = Flask(__name__)

# config
app.secret_key = 'development key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://daithi:pass1234@localhost/client_db'


db.init_app(app)


# import routes
import routes