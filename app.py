from flask import Flask, render_template, redirect, session, flash 
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, DeleteForm, FeedbackForm
from werkzeug.exceptions import Unauthorized

app = Flask(__name__) 
app.app_context().push()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///auth_ex'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False 

connect_db(app)
db.create_all() 

toolbar = DebugToolbarExtension(app) 

@app.route('/')
def main_page(): 
    return redirect('/register')

@app.route('/register', methods=['GET', 'POST'])
def register_page(): 
    form = RegisterForm()
    if form.validate() and form.is_submitted(): 
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(username, password, email, first_name, last_name)
        db.session.commit() 
        session['username'] = new_user.username
        return redirect(f"/users/{session['username']}")
    
    return render_template('register.html', form = form)

@app.route('/secret')
def secret_page(): 
    if "username" in session: 
        return redirect(f"/users/{session['username']}")
    
    else: 
        return redirect('/login')

@app.route('/login', methods=['GET', 'POST'])
def login_page(): 

    if "username" in session: 
        return redirect(f"/users/{session['username']}")

    form = LoginForm() 

    if form.validate() and form.is_submitted(): 
        username = form.username.data
        password = form.password.data 

        user = User.authenticate(username, password) 
        if user: 
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else: 
            form.username.errors = ['Invalid username/password.']
            return render_template("login_form.html", form=form)

    return render_template('login_form.html', form = form)


@app.route('/users/<username>')
def username_page(username): 
    """Example for logged in users"""

    if 'username' not in session or username != session['username']:
        raise Unauthorized() 

    user = User.query.get(username)
    form = DeleteForm() 

    return render_template("show_user.html", user=user, form=form)

@app.route('/logout')
def logout(): 
    """logout route"""

    session.pop("username")
    return redirect("/")

# ******************************************
# FEEDBACK ROUTES 
# ******************************************

@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def feedback_form(username): 
    """Add feedbacks form"""
    if 'username' not in session or username != session['username']:
        raise Unauthorized() 

    form = FeedbackForm()

    if form.validate() and form.is_submitted(): 
        title = form.title.data
        content = form.content.data 

        feedback = Feedback(
            title=title, 
            content=content, 
            username=username
        )

        db.session.add(feedback) 
        db.session.commit()

        return redirect(f"/users/{feedback.username}")
 
    return render_template("add_feedback_form.html", form = form )  

@app.route('/users/<username>/delete', methods=["post"])
def remove_user(username):
    """Remove user and redirect to login"""

    if "username" not in session or username != session['username']:
        raise Unauthorized()

    user = User.query.get(username) 
    db.session.delete(user)
    db.session.commit() 
    session.pop('username')

    return redirect('/login')

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id): 
    """ Delete feedback """
    feedback = Feedback.query.get(feedback_id)
    username = feedback.username

    # if "username" not in session or feedback.username != ['username']: 
    #     raise Unauthorized() 

    form = DeleteForm() 

    if form.validate() and form.is_submitted():
        db.session.delete(feedback) 
        db.session.commit()

    return redirect(f'/users/{feedback.username}')


@app.route('/feedback/<int:feedback_id>/update', methods=['POST', 'GET'])
def update_feedback(feedback_id):
    """Show update-feedback form and process it"""

    feedback = Feedback.query.get(feedback_id)

    if 'username' not in session or feedback.username != session['username']:
        raise Unauthorized() 

    form = FeedbackForm(obj=feedback) 

    if form.is_submitted() and form.validate(): 
        feedback.title = form.title.data 
        feedback.content = form.content.data 

        db.session.commit() 

        return redirect(f'/users/{feedback.username}')

    return render_template("edit.html", form=form, feedback=feedback)

