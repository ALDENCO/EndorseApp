from flask import Flask, request, redirect, render_template, session, flash
from app import app, db
from models import User, Advocate
import cgi


#app = Flask(__name__)

#app.config['DEBUG'] = True

@app.route('/')
def index():
    #return render_template('login.html')
    if user_is_logged_in():
        return redirect('somewheree else')
    return redirect('/login')


@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = User.query.filter_by(email=email)

@app.route('/register', methods = ['GET','POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name'] # user sending information / filling out information
        last_name = request.form['last_name']
        male = request.form['male']
        female = request.form['female']
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        #owner = request.arg.get('user']
        pw_hash = create_pw_hash(password) #here I'm taking the information captured from the form and declaring what columns it needsto go in in teh databaase
        db.session.add(User)
            #email=email,
            #first_name=first_name,
            #password=pw_hash,
        
        if password != verify:
            return redirect('/register')
        user = User(email = email,
                password=password,
                owner = owner)
                
        #     ...
        # ))
        db.session.commit()
        session['user'] = user.email
        return redirect ('/profile')
    else:
        return render_template('register.html')

@app.route('/profile', methods = ['GET'])
def profile(): #if logged in, the profile should display the information stored in the user table of the database, if not logged in redirect them to login 
    # owner = request.args.get('user')
    # if owner:
    #     users = User.query.filter_by(owner_id=owner).first()

    #     profile = every column in user table 
    # #else:
    #     #return redirect ('/login') # TODO: error handling
   
    # return render_template('profile.html', users= users, owner = owner)
    

    #what is the current loggedin  users id? get it from the session 
    #create a variable that defines / or equals user
    # #get the blog from the database using the ID!!!!
    #user_id = request.args.get('user_id')
    user_id = 1
    user = User.query.filter_by(id=user_id).first() #.first says find the first matching item / data in that database's table
    first_name = User.first_name
    last_name = User.last_name 

    advocate_id = 1
    advocate = Advocate.query.filter_by(id=advocate_id).first()
    endorsement_text = Advocate.endorsement_text
    picture_url = Advocate.picture_url
    # this pulled from blogs, is an example of what I need to happen for my users from the user table
    
    return render_template('profile.html', user = user, advocate = advocate , endorsement_text = endorsement_text, picture_url = picture_url, first_name = first_name, last_name = last_name)

@app.route('/endorse', methods = ['POST', 'GET'])
def endorse(): #similar to registter, first thing is user gets empty form that means I need a get & a post
    if request.method == 'POST':
        endorsement_text = request.form['endorsement_text']
        picture_url = request.form['picture_url']
        advocate = Advocate(text = 'endorsement_text')
        db.session.add(advocate)
        db.session.commit()
    
        user_id = 1
        user = User.query.filter_by(id=user_id).first() #.first says find the first matching item / data in that database's table
        first_name = user.first_name
        last_name = user.last_name 

        advocate_id = 1    
        advocate = Advocate.query.filter_by(id=advocate_id).first()
        endorsement_text = advocate.endorsement_text
        picture_url = advocate.picture_url
    else:
        return redirect ('/endorse')
    return render_template('profile.html', advocate = advocate, user = user, first_name = first_name, last_name = last_name, endorsement_text = endorsement_text)
    
@app.route('/endorsed', methods = ['GET'])
def endorsed():
   if email in session:
    return render_template('endorsed.html')

@app.route('/request_endorsement', methods = ['POST'])
def request_endorsement():
    if email in session:
        print("email sent")
    return render_template('request_endorsement.html')


if __name__ == "__main__":
    app.run()