
from app import db #from app.py import my database


class User(db.Model): #defines the class User as a table value in my database
    id = db.Column(db.Integer, primary_key=True) #identifies id as a column value, an integer, and the primary key value for the ORM multirelational database
    first_name = db.Column(db.String(120)) #no more than 120 character string
    last_name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    email = db.Column(db.String(120), unique= True) #all email values must be unique; no repeat values
    password = db.Column(db.String(120))
    advocates = db.relationship('Advocate',backref = 'owner', lazy=True) #this tells the database that there is a relationship between the two tables Advocate & User; the advocate stores the foreign key value aka the owner id for the two tables



    def __repr__(self):     #repr says that self be called where it will be returned with User as a placeholder of self.email
        return '<User {}>'.format(self.email)


class Advocate(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    endorsement_text = db.Column(db.Text)
    picture_url = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey ('user.id')) # the owner should equate to the user.id value; the foreign_key will be assigned this value also; 
    

    
    def __repr__(self): #self be called where it will be returned with Advocate as the placeholder of self.email
        return '<Advocate {}>' .format(self.email)