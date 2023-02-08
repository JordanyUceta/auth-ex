from flask_sqlalchemy import SQLAlchemy 
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

db = SQLAlchemy() 

def connect_db(app): 
    """Connect to database"""

    db.app = app 
    db.init_app(app) 

class User(db.Model): 

    __tablename__ = 'users' 

    # id = db.Column(db.Integer, primary_key = True, autoincrement = True) 

    username = db.Column(db.String(20), unique=True, nullable = False, primary_key= True,) 
    password = db.Column(db.Text, nullable = False) 
    email = db.Column(db.String(50), unique = True) 
    first_name = db.Column(db.String(30), nullable = False) 
    last_name = db.Column(db.String(30), nullable = False) 

    feedback = db.relationship("Feedback", backref='user', cascade='all,delete')

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register a user and also hashing their password"""

        hashed = bcrypt.generate_password_hash(password) 
        hashed_utf8 = hashed.decode("utf8")
        user = cls(
            username=username, 
            password=hashed_utf8, 
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(user) 
        return user

    @classmethod
    def authenticate(cls, username, pwd): 
        """Validate that the user exist and that the password is also correct, 
        
        return user if valid; else return false"""

        u = User.query.filter_by(username=username).first() 

        if u and bcrypt.check_password_hash(u.password, pwd): 
            # return user 
            return u 
        else: 
            return False

class Feedback(db.Model):
    """Feedback model"""

    __tablename__ = 'feedback'

    id = db.Column(db.Integer, primary_key=True) 
    title = db.Column(db.String(150), nullable=False) 
    content = db.Column(db.Text, nullable=False) 
    username = db.Column(
        db.String(20), 
        db.ForeignKey('users.username'), 
        nullable=False, 
    )