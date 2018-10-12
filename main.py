from flask import Flask, request, redirect, render_template, session, flash
from app import app, db
from models import User, Advocate
import cgi



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
                return redirect("/")
        flash('bad username or password')
        return redirect("/login")
def is_email(string):
    atsign_index = string.find('@')
    atsign_present = atsign_index >= 0
    if not atsign_present:
        return False
    else:
        domain_dot_index = string.find('.', atsign_index)
        domain_dot_present = domain_dot_index >= 0
        return domain_dot_present

def send_email():
    return (f"To:{advocate.email} Subject: {user.email} is requesting you endorse them")

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
        return redirect("/profile")
    # else:
    #     return render_template('register.html')
@app.route('/profile', methods = ['GET'])
def profile(): #if logged in, the profile should display the information stored in the user table of the database, if not logged in redirect them to login 
    owner = request.args.get('user')
    if owner:
        advocates = Advocate.query.filter_by(owner_id=owner).all()
  
    users = User.query.all()
    advocates = Advocate.query.all()
    return render_template('index.html', advocates = advocates, users = users, owner = owner)

    #     profile = every column in user table  #get isn't allowed to change information; post is allowed to change information
    # #else:
    #     #return redirect ('/login') # TODO: error handling
   
    

    #what is the current loggedin  users id? get it from the session 
    #create a variable that defines / or equals user
   
    
   

@app.route('/request_endorsement', methods = ['GET'])
def view_empty_request_endorsement_form():
    return render_template('request_endorsement.html')

@app.route('/request_endorsement', methods = ['POST'])
def send_request_endorsement_form():
    email = request.form['email']
    user_id = session['user_id']
    
    user = User(first_name = first_name, last_name = last_name)
    advocate = Advocate(email = email, owner_id = user_id)
    db.session.add(advocate)
    db.session.commit()
    return (f"To:{advocate.email} Subject: {user.first_name} {user.last_name} is requesting you endorse them")
    #return (send_email) #(f"{advocate.email} email sent here")
    #return redirect('/request_endorsement')

@app.route('/endorse/<advocate_id>', methods=['GET'])
def now_view_empty_endorsement_form(advocate_id):
    return render_template('endorse.html', advocate_id = advocate_id)


@app.route('/endorse/<advocate_id>', methods = ['POST'])
def submit_endorsement(advocate_id): 
    endorsement_text = request.form['endorsement_text']
    picture_url = request.form['picture_url']
  
    advocate = Advocate.query.get(advocate_id)
    advocate.endorsement_text = endorsement_text
    advocate.picture_url = picture_url
    db.session.add(advocate)
    db.session.commit()
    session['advocate'] = advocate.email
    return redirect(f'/endorsed/{advocate_id}')

@app.route('/endorsed/<advocate_id>', methods = ['GET'])
def endorsed(advocate_id):
    advocate = Advocate.query.filter_by(id=advocate_id).first()
    return render_template('endorsed.html', advocate = advocate)

if __name__ == "__main__":
    app.run()



   