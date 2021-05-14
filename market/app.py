
from flask import Flask
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.db'
app.config['SECRET_KEY'] = 'e49f7898dcafbe0db7e81abf'

bcrypt = Bcrypt(app)
