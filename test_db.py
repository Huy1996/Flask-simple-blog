from flask import Flask
from sqlalchemy.exc import IntegrityError
from db import db, User, Post
import pytest


@pytest.fixture(autouse=True)
def set_up():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test/test.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.app_context().push()
    db.init_app(app)
    db.create_all()
    yield db
    db.drop_all()


@pytest.fixture
def john_info():
    return {
        "username": "John Doe",
        "email": "john@example.com",
        "password": "password"
    }


@pytest.fixture
def john(john_info):
    user = User(**john_info)
    user.save_to_db()
    return user


@pytest.fixture
def john_post(john):
    return {
        "title": "test title",
        "content": "This is a test content of the blog.",
        "user_id": john._id
    }


@pytest.fixture
def john_post_list(john):
    post_list = [
        {
            "title": "title 1",
            "content": "This is a test content of the blog.",
            "user_id": john._id
        },
        {
            "title": "title 2",
            "content": "This is a test content of the blog.",
            "user_id": john._id
        },
        {
            "title": "title 3",
            "content": "This is a test content of the blog.",
            "user_id": john._id
        }
    ]
    for entry in post_list:
        post = Post(**entry)
        post.save_to_db()

    return post_list


@pytest.fixture
def sample_post(john_post):
    post = Post(**john_post)
    post.save_to_db()
    return post


def test_find_post(sample_post, john_post, john):
    post = Post.find_by_id(sample_post._id)
    assert post.title == john_post["title"]
    assert post.content == john_post["content"]
    assert post.user_id == john._id
    assert post.user == john


def test_empty_title_post(john_post):
    post = Post(None, john_post["content"], john_post['user_id'])
    with pytest.raises(IntegrityError):
        post.save_to_db()
    db.session.rollback()


def test_unique_email(john_info, john):
    user = User(
        username="Test Name",
        email=john_info['email'],
        password="test123"
    )
    with pytest.raises(IntegrityError):
        user.save_to_db()
    db.session.rollback()


def test_unique_username(john_info, john):
    user = User(
        username=john_info['username'],
        email="test@example.com",
        password="test123"
    )
    with pytest.raises(IntegrityError):
        user.save_to_db()
    db.session.rollback()


def test_find_user_by_email(john_info, john):
    user = User.find_by_email(john_info["email"])
    assert user == john


def test_get_user_post(john, john_post_list):
    john = User.find_by_id(john._id)
    assert len(john.posts) == len(john_post_list)
