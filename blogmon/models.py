from flask import current_app
from blogmon import db, login_manager
from itsdangerous import URLSafeTimedSerializer as Serializer
from flask_login import UserMixin
from sqlalchemy import func

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(30), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    date_joined = db.Column(db.DateTime, default=func.now())    
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')

    # one to many relationship
    posts = db.relationship('Post', backref='author', lazy=True)

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'user_id': self.id}, salt='password-reset-salt')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token, salt='password-reset-salt', max_age=1800)['user_id']
        except:
            return None
        return User.query.get(user_id)


    # string representation of a class
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.date_joined}', '{self.image_file}')"

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, default=func.now())  
    content = db.Column(db.Text, nullable=False)  
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.title}', '{self.date_posted}', '{self.content}')"
