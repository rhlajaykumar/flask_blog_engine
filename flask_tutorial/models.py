from datetime import datetime
# login manager manges the user session
from flask_tutorial import db, login_manager
# to provide fuctionality like is_user_active, etc
from flask_login import UserMixin

# registers a session to login manager with the given user id
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))



# creates a table with table_name lowercase user
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(200), nullable=False)
    # here Post is referencing to Post class not post table in db
    posts = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # user in user.id is in lowercase because it references to user table which is in lowercase
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Title('{self.title}', '{self.date_posted}')"
