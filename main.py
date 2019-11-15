from flask import Flask, request, redirect, render_template, session, flash
from app import app, db
from models import User, Advocate
from itsdangerous import URLSafeSerializer
import cgi
import requests
import os
from flask_debugtoolbar import DebugToolbarExtension


@app.route('/home', methods = ['GET'])
def view_blank_homepage():
    return render_template('home.html')


@app.route('/', methods = ['GET'])
def index():
    return render_template('home.html') #I've rerouted the index file to the home.html template
    # owner = request.args.get(["user"])
    # if owner:
    #     advocates = Advocate.query.filter_by(owner_id=owner).all()
  
    # user = User.query.all()
    # advocates = Advocate.query.all()
    # return render_template('index.html', advocates = advocates, user = user, owner = owner)
    #return render_template('login.html')
    # if user_is_logged_in():
    #     return redirect('somewheree else')
    # return redirect('/login')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET':  #the register route must first GET the register.html template
        # print("getting") shows that the GET method worked in terminal
        print("HERE AGAIN?")
        return render_template('register.html')
    elif request.method == 'POST':
        # print("aint doing shit")
        first_name = request.form['first_name'] # user sending information / filling out information
        last_name = request.form['last_name'] #request.form says grab user input from last_name and add to database
        age = request.form['age']
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        owner = request.args.get('user') #assign a user an owner foreign key value
        user = User(email = email, first_name = first_name, last_name = last_name, age = age, password = password) #identifies each form value as equaling its corresponding value in the database
        db.session.add(user) #officially adds the user of that session as defined above to the database
        db.session.commit() #commits/saves that user to the database permanently 
        session['user'] = user.email  #session is defined as a user via user email
        print("ARE WE HERE?")
        # session['user_id'] = user.id
        # user_id = session['user_id'] #defining the user_id by the user.id that is already logged in / in session in the database
        users = User.query.filter_by(email=email)
        user_id = User.query.get(user.id) # get the user from the database
        advocates = user.advocates # any advocate must be owned / linked/ invited by the user in session
        return redirect (f'profile/{user.id}')

@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users = User.query.filter_by(email=email) #get the user from the database; defined as the email entered into the login form corresponding to the same value stored in the database
        if users.count() == 1: #only one user (as defined by their unique email) can exist in this database
            user = users.first() #find the first instance of the user that matches the data requested by the login form
            if password == user.password: #if the password entered matches the password stored in the database
                session['user_id'] = user.id #resume the session of that user.id
                flash('welcome back, '+user.email) 
                return redirect(f'profile/{user.id}') #take that user to their personal profile
        flash('bad username or password')
        return render_template("/register") #else return the user to the register template as there data is not verified by the database
        
def is_email(string): #define an email as a string that must include an @ sign
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index) #additionally an email is recognized as containing a .domain 
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present


@app.route('/profile', methods = ['GET'])
def logged_in_user_profile():
    if 'user_id' not in session:  #if the user is not already in session (aka logged in), return them to the login template
        print(user_id)
        return redirect("login.html")
    user_id = session['user_id'] #defining the user_id by the user.id that is already logged in / in session in the database
    user = User.query.get(user_id) # get the user from the database
    advocates = user.advocates  # any advocate must be owned / linked/ invited by the user in session
    # print("first advocate:", advocates[0].__dict__)
    return render_template('profile.html', users = user, advocates = advocates) #passes the user and advocate data into the profile so that it will be recognized by jinja


@app.route('/profile/<user_id>', methods = ['GET']) #only show the user who's user.id is in session; aka privacy/security
def specific_users_profile(user_id): #call that specific user id
    user = User.query.get(user_id)  #again, the user equals the user.id in session
    advocates = user.advocates  #the advocate equals the advocate as defined/invited/linked to the user in the database
    return render_template('profile.html', advocates = advocates, user=[user]) #show me that specific user's profile, only show that specific [user] from the user table

@app.route('/request_endorsement', methods = ['GET'])
def view_empty_request_endorsement_form():
    user_id = session['user_id']
    user = User.query.get(user_id)
    
    return render_template('request_endorsement.html', user=[user])
SafeSerializer = URLSafeSerializer('advocate_id') # itsdangerous safeserializer is assigning a random key value to the advocate id for security purposes (so anybody from the peanut gallery can't hack another's profile



@app.route('/request_endorsement', methods = ['POST'])
def send_request_endorsement_form():
    email = request.form['email']
    user_id = session['user_id']
    user = User.query.first()
    advocate = Advocate(email = email, owner_id = user_id) #the advocate is defined by the email from the form input, the owner id, owned by the advocate, is equal to the user id value
    db.session.add(advocate) #create a new session, defined by the advocate now
    db.session.commit()
    #import pdb; pdb.set_trace() #stops code at this point so that I may ensure specific methods have completed successfully 
    concealed_adv_id = SafeSerializer.dumps(advocate.id) # the created advocate id is defined by the value created by the safe serializer aka the conceald advocate id
    print(concealed_adv_id)

    url = ("https://api.mailgun.net/v3/www.alexrmyers.com/messages") #mailgun api url categorized by JSON parameters
    auth=('api', os.getenv('API_KEY')) #the api, as recognized by JSON, is populated by calling the environmental variable via the OS, the api key value identified as API_KEY
    print("POSTING") #debugging message showing that the POST method is successful to this point
    data={"from": "postmaster@www.alexrmyers.com",
            "to": [f"{advocate.email}"],
            "subject": "Hello",
            "text": f"{user.first_name} {user.last_name} is requesting your endorsement! https://encourageapp.herokuapp.com/endorse/{concealed_adv_id}"}
    response = requests.post(url , auth = auth, data = data) #the api response initiatied by the python requests library
    resp = response.content #the api response equals the exact content of that response
    return redirect(f'profile/{user.id}')

@app.route('/endorse/<concealed_advocate_id>', methods=['GET'])
def now_view_empty_endorsement_form(concealed_advocate_id):
    advocate_id = SafeSerializer.loads(concealed_advocate_id) #the empty endorsement form is served only to the email address of the defined concealed advocate id
    return render_template('endorse.html', advocate_id=advocate_id, concealed_advocate_id=concealed_advocate_id) #identifies database values for jinja
    


@app.route('/endorse/<concealed_advocate_id>', methods=['POST'])
def submit_endorsement(concealed_advocate_id):
    advocate_id = SafeSerializer.loads(concealed_advocate_id)
    endorsement_text = request.form['endorsement_text']
    picture_url = request.form['picture_url']
    

    advocate = Advocate.query.get(advocate_id)
    user = advocate.owner
    advocate.endorsement_text = endorsement_text
    advocate.picture_url = picture_url
    db.session.add(advocate)
    db.session.commit()
    session['advocate'] = advocate.email #define the session as unique to that advocate's email

    url = ("https://api.mailgun.net/v3/www.alexrmyers.com/messages")
    auth=('api', os.getenv('API_KEY'))
    data={"from": "postmaster@www.alexrmyers.com",
            "to": [f"{user.email}"],
            "subject": "Hello",
            "text": f"{advocate.email} has endorsed you! https://encourageapp.herokuapp.com/profile/{user.id}"}
    response = requests.post(url, auth=auth, data=data)
    resp = response.content    
    return redirect(f'/endorsed/{concealed_advocate_id}')

@app.route('/endorsed/<concealed_advocate_id>', methods = ['GET'])
def endorsed(concealed_advocate_id):
    advocate_id = SafeSerializer.loads(concealed_advocate_id)
    advocate = Advocate.query.filter_by(id=advocate_id).first()
    user = advocate.owner
    return render_template('endorsed.html', advocate = advocate, user = user, advocate_id = advocate_id, concealed_advocate_id = concealed_advocate_id)

@app.route('/invite', methods = ['GET'])
def view_empty_user_invite_form():
    user_id = session['user_id']
    user = User.query.get(user_id)
    return render_template('invite.html', user=[user])


@app.route('/invite', methods = ['POST'])
def send_user_invite_form():
    email = request.form['email']
    user = User.query.first()
    #import pdb; pdb.set_trace()
    # if user in session:
    #     print(yes)

    url = ("https://api.mailgun.net/v3/www.alexrmyers.com/messages")
    auth=('api', os.getenv('API_KEY'))
    data={"from": "postmaster@www.alexrmyers.com",
            "to": [f"{email}"],
            "subject": "Hello",
            "text": f"{user.first_name} {user.last_name} wants you to join their social circle! https://encourageapp.herokuapp.com/register"}
    response = requests.post(url , auth = auth, data = data)
    resp = response.content
    # resp = response.json
    # print(response.content)
    return redirect(f'profile/{user.id}')


@app.route('/logout', methods=['GET','POST']) 
def logout():
    # print(user_id)
    session.pop('user_id', None) #pop that user.id out of session and make the value none so that no user is in session
    print(session.get('user_id'))
    return redirect('/home') #redirect that user to the login form to create a new session


if __name__ == "__main__": #if the name of the file is main, run the app
    app.run()