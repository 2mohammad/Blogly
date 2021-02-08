from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app): 
    db.app = app
    db.init_app(app)



# MODELS GO BELOW

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