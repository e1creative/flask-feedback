"""Flask app for Feedback"""

from flask import Flask, request, render_template, redirect, flash, session, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_bcrypt import Bcrypt
from models import db, connect_db, User, Feedback

from forms import UserForm, FeedbackForm, LoginForm

app = Flask(__name__)
bcrypt = Bcrypt()


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "chickenzarecool21837"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)

connect_db(app)
# db.create_all()

@app.route('/')
def show_home_page():
    """Redirect to /register."""
    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    """Show a form that when submitted will register/create a user. 
    This form should accept a username, password, email, first_name, and last_name.
    Make sure you are using WTForms and that your password input 
    hides the characters that the user is typing!"""
    """Process the registration form by adding a new user. Then redirect to the users detail page"""

    form = UserForm()

    if form.validate_on_submit():
        u = request.form.get('username')
        p = request.form.get('password')
        e = request.form.get('email')
        fn = request.form.get('first_name')
        ln = request.form.get('last_name')
        
        new_user = User.register(u, p, e, fn, ln)

        print('')
        print('********************')
        print('new_user: ', new_user)
        print('********************')
        print('')

        db.session.add(new_user)
        db.session.commit()

        return redirect(f'/users/{new_user.username}')

    print(form.errors)
    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Show a form that when submitted will login a user. This form should accept a username and a password.
    Make sure you are using WTForms and that your password input hides the characters that the user is typing!"""

    """Process the login form, ensuring the user is authenticated and going to the users home page if so."""

    form = LoginForm()

    if form.validate_on_submit():
        username = request.form.get('username')
        password = request.form.get('password')

        # throw a 404 if the user doesn't exist
        try:
            user = User.query.get_or_404(username)
        except:
            flash(message = f"Username doesn't exist!")
            return redirect('/login')

        # bcrypt password checking        
        authenticated_user = User.authenticate(username, password)

        print('')
        print('********************')
        print('password_match: ', authenticated_user)
        print('********************')
        print('')


        if authenticated_user:
            # if user is authenticated, set the username to the session variable
            username = authenticated_user.username
            session['username'] = username
            # redirect to the user's detail page
            return redirect(f'/users/{username}')
        else:
            # if user is not authenticated, flash them a message and redirect to login
            flash(message = f"Incorrect Password")
            return redirect('/login')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Clear any information from the session and redirect to / """

    session.clear()
    flash(message='You have been logged out!')

    return redirect('/')



################### USERS & FEEDBACK ROUTES ###################

# protected route, only logged in users should be able to acees this
@app.route('/users/<username>')
def show_user_detail(username):
    """Show information about the given user. (everything except for their password)
        
    You should ensure that only logged in users can access this page.

    Show all of the feedback that the user has given.
    
    For each piece of feedback, display with a link to a form to edit the feedback and a 
    button to delete the feedback.
    
    Have a link that sends you to a form to add more feedback and 
    a button to delete the user Make sure that only the user who is logged in can successfully view this page."""


    # check if there is a session, if not redirect to login
    try: 
        logged_in_username = session.get('username')
    except:
        return redirect('/login')


    # if there is a session check if there if the logged in user 
    # is the same as the user attempting to be accessed
    if logged_in_username == username:
        print('')
        print('********************')
        print('user: ', logged_in_username)
        print('********************')
        print('')

        user = User.query.get(username)
        return render_template('user-detail.html', user=user)
    else: 
        return redirect('/logout')

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """Remove the user from the database and make sure to also delete all of their feedback.
    Clear any user information in the session and redirect to /. 
    Make sure that only the user who is logged in can successfully delete their account"""

    # check if a user is logged in AND
    #  the logged in user is the same as the user attempting to be deleted
    if session.get('username') and session.get('username') == username:        
        #delete the user
        User.query.filter_by(username=username).delete()
        db.session.commit()

        #clear the session
        session.clear()

    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET', 'POST'])
def feedback_form(username):
    """Display a form to add feedback Make sure that only the user who is logged in can see this form"""
    form = FeedbackForm()

    if username != session.get('username'):
        return redirect('/logout')

    if form.validate_on_submit():
        title = request.form.get('title')
        content = request.form.get('content')

        new_feedback = Feedback(title=title, content=content, username=username)

        db.session.add(new_feedback)
        db.session.commit()

        return redirect(f'/users/{username}')

    return render_template('add-feedback.html', username=username, form=form)



    """Add a new piece of feedback and redirect to /users/<username> 
    — Make sure that only the user who is logged in can successfully add feedback"""


@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def edit_feedback_form(feedback_id):
    """Display a form to edit feedback — 
    **Make sure that only the user who has written that feedback can see this form **"""
    """Update a specific piece of feedback and redirect to /users/<username> 
    — Make sure that only the user who has written that feedback can update it"""

    # if no user is logged in, redirect to the login page
    if not session.get('username'):
        return redirect('/login')

    f = Feedback.query.get(feedback_id)
    form = FeedbackForm(obj=f)

    logged_in_username = session.get('username')

    # if user is logged in, check that the username for the feedback is the same as the
    # username for the session
    if f.username != logged_in_username:
        return redirect(f'/users/{logged_in_username}')

    # if username for the feedback IS the same as the logged in user
    # then we continute below
    if form.validate_on_submit():
        f.title = request.form.get('title')
        f.content = request.form.get('content')

        db.session.commit()

        return redirect(f'/users/{f.username}')

    return render_template('edit-feedback.html', form=form, feedback_id=feedback_id)



@app.route('/feedback/<feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    """Delete a specific piece of feedback and redirect to /users/<username> 
    — Make sure that only the user who has written that feedback can delete it"""

    f = Feedback.query.get(feedback_id)
    username = f.username

    # check if a user is the owner of the feedback that is trying to be deleted
    if session.get('username') == username:
        # delete the feedback
        db.session.delete(f)
        db.session.commit()
        return redirect(f'/users/{username}')
            
    return redirect('/')
