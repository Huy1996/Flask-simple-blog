from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import Flask

db = SQLAlchemy()

app = Flask(__name__)

app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'

app.app_context().push()
db.init_app(app)
db.create_all()


class Base(db.Model):
    __abstract__ = True

    _id = db.Column(db.Integer, primary_key=True, unique=True)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(_id=_id).first()

    @classmethod
    def get_all_data(cls):
        return cls.query.all()

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Post(Base):
    __tablename__ = "post"

    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user._id'), nullable=False)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id


class User(Base):
    __tablename__ = "user"

    username = db.Column(db.String(255), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    admin = db.Column(db.Boolean(), default=False, nullable=False)
    posts = db.relationship("Post", backref="user")

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
