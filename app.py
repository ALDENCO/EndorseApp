import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension
import psycopg2 #psycopg2 is crucial to postgres
from flask_migrate import Migrate #flask migrate allows for easy migration of databases between development and production environments


app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgres://localhost/endorseme') #this tells postgres to connect to my database entitled endorseme
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgres://fqjbxepzavucck:f70d06903408cdaaf6521815a3239d9dc91a3ba41bef22373b4930596bcf6389@ec2-54-204-14-96.compute-1.amazonaws.com:5432/d694lvm48j7s2l') #identity of my heroku postgres database
app.config['SQLALCHEMY_ECHO'] = True
app.config['SESSION_TYPE'] = 'memcached'
app.config['SECRET_KEY'] = 'secret key' #make cookie sessions into secure/unintendifiable secret key values
app.config['API_KEY'] = os.getenv('API_KEY') #tells python to identify the API_KEY as set in en environmental variable (.env file that is identified in the git ignore)
app.debug = False #set to True to re-enable the DebugToolbar


toolbar = DebugToolbarExtension(app)
db = SQLAlchemy(app) #tells my app that SQLAlchemy is my SQL framework and to identify my database as db
migrate = Migrate(app, db) 
