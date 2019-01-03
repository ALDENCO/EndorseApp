from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(120))
    last_name = db.Column(db.String(120))
    age = db.Column(db.Integer)
    email = db.Column(db.String(120), unique= True)
    password = db.Column(db.String(120))
    advocates = db.relationship('Advocate',backref = 'owner', lazy=True) #this tells the database that there is a relationship between the two tables Advocate & User



    def __repr__(self):     #repr says that self be called where it will be returned with User as a placeholder of self.email
        return '<User {}>'.format(self.email)


class Advocate(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120))
    endorsement_text = db.Column(db.Text)
    picture_url = db.Column(db.Text)
    owner_id = db.Column(db.Integer, db.ForeignKey ('user.id')) # the owner should equate to the user.id value; the foreign_key will be assigned this value also; 
    

    
    def __repr__(self):
        return '<Advocate {}>' .format(self.email)



