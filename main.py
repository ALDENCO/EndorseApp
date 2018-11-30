from flask import Flask, request, redirect, render_template, session, flash
from app import app, db
from models import User, Advocate
from itsdangerous import URLSafeSerializer
import cgi
import requests
import os


@app.route('/home', methods = ['GET'])
def view_blank_homepage():
    return render_template('home.html')


@app.route('/', methods = ['GET'])
def index():

    owner = request.args.get('user')
    if owner:
        advocates = Advocate.query.filter_by(owner_id=owner).all()
  
    users = User.query.all()
    advocates = Advocate.query.all()
    return render_template('index.html', advocates = advocates, users = users, owner = owner)
    #return render_template('login.html')
    # if user_is_logged_in():
    #     return redirect('somewheree else')
    # return redirect('/login')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'GET': #the register route must first get the register html template
        return render_template('register.html')
    elif request.method == 'POST':
        first_name = request.form['first_name'] # user sending information / filling out information
        last_name = request.form['last_name']
        age = request.form['age']
        email = request.form['email']
        password = request.form['password']
        verify = request.form['verify']
        owner = request.args.get('user')
        if not is_email(email):
            flash('zoiks! "' + email + '" does not seem like an email address')
            return redirect('/register')
        #email_db_count = User.query.filter_by(email=email).count()
       # if email_db_count > 0:
            #flash('yikes! "' + email + '" is already taken and password reminders are not implemented')
            #return redirect('/register')
        if password != verify:
            flash('passwords did not match')
            return redirect('/register')
        user = User(email = email, first_name = first_name, last_name = last_name, age = age, password = password)
        db.session.add(user)
        db.session.commit()
        session['user'] = user.email
        return render_template('login.html')
    # else:
    #     return redirect("/register")


@app.route('/login', methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = User.query.filter_by(email=email)
        if users.count() == 1:
            user = users.first()
            if password == user.password:
                session['user_id'] = user.id
                flash('welcome back, '+user.email)
                return redirect(f'profile/{user.id}')
        flash('bad username or password')
        return render_template("/register")
   
        
def is_email(string):
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present

@app.route('/profile', methods = ['GET'])
def logged_in_user_profile():
    if 'user_id' not in session: #user is logged in, send them somewhere else
        return redirect("login.html")
    user_id = session['user_id']
    user = User.query.get(user_id) # get the user from the database
    advocates = user.advocates
    return render_template('profile.html', user=user, advocates = advocates)


@app.route('/profile/<user_id>', methods = ['GET'])
def specific_users_profile(user_id):
    user = User.query.get(user_id)
    advocates = user.advocates
    return render_template('profile.html', advocates = advocates, users = [user])

@app.route('/request_endorsement', methods = ['GET'])
def view_empty_request_endorsement_form():
    return render_template('request_endorsement.html')

SafeSerializer = URLSafeSerializer('advocate_id')


@app.route('/request_endorsement', methods = ['POST'])
def send_request_endorsement_form():
    email = request.form['email']
    user_id = session['user_id']
    user = User.query.first()
    advocate = Advocate(email = email, owner_id = user_id)
    db.session.add(advocate)
    db.session.commit()
    #import pdb; pdb.set_trace()
    concealed_adv_id = SafeSerializer.dumps(advocate.id)
  

    url = ("https://api.mailgun.net/v3/sandboxbb3c57abd2b74c158f41c341ba91123b.mailgun.org/messages")
    auth=("api", os.getenv('api_key'))
    data={"from": "Alex Myers <mailgun@sandboxbb3c57abd2b74c158f41c341ba91123b.mailgun.org>",
            "to": [f"{advocate.email}"],
            "subject": "Hello",
            "text": f"{user.first_name} {user.last_name} is requesting your endorsement! http://localhost:5000/endorse/{concealed_adv_id}"}
    response = requests.post(url , auth = auth, data = data)
    #print(response)
    resp = response.json()
    return redirect(f'profile/{user.id}')

@app.route('/endorse/<concealed_advocate_id>', methods=['GET'])
def now_view_empty_endorsement_form(concealed_advocate_id):
    advocate_id = SafeSerializer.loads(concealed_advocate_id)
    return render_template('endorse.html', advocate_id = advocate_id, concealed_advocate_id = concealed_advocate_id)


@app.route('/endorse/<concealed_advocate_id>', methods = ['POST'])
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
    session['advocate'] = advocate.email
    url = ("https://api.mailgun.net/v3/sandboxbb3c57abd2b74c158f41c341ba91123b.mailgun.org/messages")
    auth=("api", os.getenv('api_key'))
    data={"from": "Alex Myers <mailgun@sandboxbb3c57abd2b74c158f41c341ba91123b.mailgun.org>",
            "to": [f"{user.email}"],
            "subject": "Hello",
            "text": f"{advocate.email} has endorsed you! http://localhost:5000/profile/{user.id}"}
    response = requests.post(url , auth = auth, data = data)
    #print(response)
    resp = response.json()
    return redirect(f'/endorsed/{concealed_advocate_id}')

@app.route('/endorsed/<concealed_advocate_id>', methods = ['GET'])
def endorsed(concealed_advocate_id):
    advocate_id = SafeSerializer.loads(concealed_advocate_id)
    advocate = Advocate.query.filter_by(id=advocate_id).first()
    user = advocate.owner
    return render_template('endorsed.html', advocate = advocate, user = user)

@app.route("/logout", methods=['POST'])
def logout():
    del session['user']
    return redirect("/login")


if __name__ == "__main__":
    app.run()



   