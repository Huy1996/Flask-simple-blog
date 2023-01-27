"""
This module contains a database schema
"""

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


class Base(db.Model):
    """
    An abstract class that contain common field of table and
    function to support search, save, and delete entry
    """
    __abstract__ = True

    _id = db.Column(db.Integer, primary_key=True, unique=True)
    created_on = db.Column(db.DateTime(), default=datetime.now)
    updated_on = db.Column(db.DateTime(), default=datetime.now, onupdate=datetime.now)

    @classmethod
    def find_by_id(cls, _id):
        """
        Find data in database by it's id
        :param _id: id of the data want to find
        :return:
        """
        return cls.query.filter_by(_id=_id).first()

    @classmethod
    def get_all_data(cls):
        """
        Get all data of the table
        :return: list of data
        """
        return cls.query.all()

    def save_to_db(self):
        """
        Save (update or create) data to database
        :return: None
        """
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        """
        Delete data from database
        :return: None
        """
        db.session.delete(self)
        db.session.commit()


class Post(Base):
    """
    Post table contain all the blogs that user posted
    """
    __tablename__ = "post"

    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(1000), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user._id'), nullable=False)

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id


class User(Base):
    """
    User table contain the information of all the user
    """
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

    @classmethod
    def find_by_email(cls, email):
        """
        Find user by their email
        :param email: email of user
        :return: user
        """
        return cls.query.filter_by(email=email).first()
