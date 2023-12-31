from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


class User(db.Model):
    __tablename__: str = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password= db.Column(db.String(20), nullable=False)


class Post(db.Model):
    __tablename__: str = 'post'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    content = db.Column(db.String(1000))
    datetime = db.Column(db.DateTime, default=datetime.now(), onupdate=datetime.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="SET NULL"), nullable=True)
    user = db.relationship('User', backref=db.backref('post_user_set'))

class Comment(db.Model):
    __tablename__ = 'comment'

    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete="CASCADE"))
    post = db.relationship('Post', backref=db.backref('comment_set'))

    content = db.Column(db.Text(), nullable=False)
    datetime = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="SET NULL"), nullable=True)
    user = db.relationship('User', backref=db.backref('comment_user_set'))
    