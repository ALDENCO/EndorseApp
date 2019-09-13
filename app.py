import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgres://localhost/endorseme') #this tells postgres to connect to my database entitled endorseme
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgres://fqjbxepzavucck:f70d06903408cdaaf6521815a3239d9dc91a3ba41bef22373b4930596bcf6389@ec2-54-204-14-96.compute-1.amazonaws.com:5432/d694lvm48j7s2l')
app.config['SQLALCHEMY_ECHO'] = True
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'secret key'
app.config['api'] = os.getenv('api')

db = SQLAlchemy(app)


