from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/endorseme' #this tells postgres to connect to my database entitled endorseme
app.config['SQLALCHEMY_ECHO'] = True

db = SQLAlchemy(app)