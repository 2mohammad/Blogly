from enum import unique
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

db = SQLAlchemy()

def connect_db(app): 
    db.app = app
    db.init_app(app)



# MODELS GO BELOW

# Blog Class
class Blog(db.Model):
    __tablename__ = 'roster'

    def __repr__(self):
        """ Provides a user defined object description """
        user = self
        return f"<User id={user.id} first_name={user.first_name} last_name={user.last_name}"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False, unique=False)
    last_name = db.Column(db.String(50), nullable=False, unique=False)
    image_url = db.Column(db.Text,  nullable=False, unique=True)

     
      
    @classmethod
    def get_all_users(cls):
        return cls.query.all()

# Post Class
class Posts(db.Model):
    """ Post: A Model for Posts. """
    __tablename__ = "posts"

    def __repr__(self):
        """ Provides a user defined object description """
        post = self
        return f"<Post id={post.id} Post title={post.title} Post User={post.user_id}"


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False, unique=False)
    content = db.Column(db.Text, nullable=False, unique=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('roster.id'))
    userID = db.relationship('Blog')


    def get_post_maker(self):
        print(self)
        post = Posts.query.get(self)
        print(post)
        user = {
            "name": f'{post.userID.first_name} {post.userID.last_name}',
            "id": post.userID.id
        }
        return (user)





