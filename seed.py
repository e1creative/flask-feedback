import bcrypt
from models import db, User, Feedback
from flask_bcrypt import Bcrypt
from app import app

bcrypt = Bcrypt()

db.drop_all()
db.create_all()

User.query.delete()
Feedback.query.delete()


##### USER #####
user1pw = bcrypt.generate_password_hash('password1')
user2pw = bcrypt.generate_password_hash('password2')

pw1 = user1pw.decode('utf8')
pw2 = user2pw.decode('utf8')

u1 = User(username='user1', password=pw1, email='userone@gmail.com', first_name='UserOne', last_name='One')
u2 = User(username='user2', password=pw2, email='usertwo@gmail.com', first_name='UserTwo', last_name='Two')

add_users = [u1, u2]

db.session.add_all(add_users)
db.session.commit()


##### FEEDBACK #####

f1 = Feedback(title='Feedback One', content='Content for feedback one.', username='user1')
f2 = Feedback(title='Feedback Two', content='Content for feedback two.', username='user2')

add_feedback = [f1, f2]

db.session.add_all(add_feedback)
db.session.commit()
