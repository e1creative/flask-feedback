"""Models for Cupcake app."""

from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
bcrypt = Bcrypt()

def connect_db(app):
    db.app = app
    db.init_app(app)


class User(db.Model):
    __tablename__ = "users"

    username = db.Column(db.String(20), primary_key=True, unique=True)
    password = db.Column(db.Text, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False )

    feedback = db.relationship('Feedback', backref='user')

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a new user with hashed password"""

        hashed = bcrypt.generate_password_hash(password)
        # turn bytestring into normal (unicode utf8) string
        hashed_utf8 = hashed.decode('utf8')

        #return instance of user w/username and hashed password
        return cls(username=username, password=hashed_utf8, email=email, first_name=first_name, last_name=last_name)

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is corret.
        Return user if valid; else return false"""

        u = User.query.filter_by(username=username).first()

        if u and bcrypt.check_password_hash(u.password, password):
            return u
        else:
            return False


    def __repr__(self):
        """Show Info about User"""
        u = self
        return f"<User id={u.username} password={u.password} email={u.email} first_name={u.first_name} last_name={u.last_name}>"


class Feedback(db.Model):
    __tablename__ =  "feedback"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    username = db.Column(db.ForeignKey(User.username), nullable=False)

    def __repr__(self):
        """Show Info about Feedback"""
        f = self
        return f"<Feedback id={f.id} title={f.title} content={f.content} username={f.username}>"