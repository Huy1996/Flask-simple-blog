from flask import Flask, request, render_template, redirect, url_for, session, make_response, flash
from db import db, Post, User
from form import PostForm, LoginForm, RegisterForm
from utils import date_filter
from sqlalchemy.exc import IntegrityError


def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = b'_5#y2L"F4Q8z\n\xec]/'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
    app.jinja_env.filters['datefmt'] = date_filter

    app.app_context().push()
    db.init_app(app)
    db.create_all()

    @app.route('/')
    def main():
        blogs = Post.get_all_data()
        return render_template('home.html', blogs=blogs)

    @app.route('/home')
    def home():
        if "user_id" in session:
            user = User.find_by_id(session.get("user_id"))
            blogs = user.posts
            return render_template('home.html', blogs=blogs)
        return render_template('home.html', login_require=True)

    @app.route('/about')
    def about():
        return render_template('about.html')

    @app.route('/admin')
    def admin():
        if session.get("admin"):
            user_list = User.get_all_data()
            return render_template('admin.html', users=user_list)
        flash("Request restricted.")
        return redirect(url_for('home'))

    @app.route('/post', methods=('GET', 'POST'))
    def post():
        form = PostForm()
        if form.validate_on_submit():
            post = Post(
                title=form.title.data,
                content=form.content.data,
                user_id=session["user_id"]
            )
            try:
                post.save_to_db()
            except IntegrityError:
                flash("Something went wrong. Please try again.")
                return render_template('post.html', form=form)
            flash("Your new blogs are posted.")
            return redirect(url_for('home'))
        return render_template('post.html', form=form)

    @app.route('/<int:id>/edit', methods=('GET', 'POST'))
    def edit(id):
        post = Post.find_by_id(id)
        form = PostForm()

        if post and session.get("user_id") == post.user_id:
            if request.method == "GET":
                form.title.data = post.title
                form.content.data = post.content
                return render_template('post.html', form=form)

            if form.validate_on_submit():
                post.title = form.title.data
                post.content = form.content.data

                try:
                    post.save_to_db()
                except IntegrityError:
                    flash("Request Fail")
                    return render_template('post.html', form=form)

                return redirect(url_for('home'))
        else:
            return "<h1>Invalid request</h1>"

    @app.route('/<int:id>/delete')
    def delete(id):
        post = Post.find_by_id(id)
        if post and (post.user_id == session.get("user_id") or session.get("admin")):
            try:
                post.delete_from_db()
            except Exception as e:
                flash(e)

            return redirect(url_for('home'))
        return '<h1>Invalid Request</h1>'

    @app.route('/logout')
    def logout():
        session.pop("username", None)
        session.pop("admin", None)
        session.pop("user_id", None)
        res = make_response(redirect(url_for('home')))
        res.delete_cookie("username")
        res.delete_cookie("email")
        return redirect(url_for('home'))

    @app.route('/register', methods=('GET', 'POST'))
    def register():
        form = RegisterForm()
        if form.validate_on_submit():
            user = User(
                username=form.username.data,
                email=form.email.data,
                password=form.password.data
            )
            try:
                user.save_to_db()
            except IntegrityError:
                flash("Email are used. Please try again")
                db.session.rollback()
                return render_template('register.html', form=form)

            return redirect(url_for('login'))

        return render_template('register.html', form=form)

    @app.route('/login', methods=('GET', 'POST'))
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            email = form.email.data
            password = form.password.data
            user = User.find_by_email(email)
            if user and user.password == password:
                session["username"] = user.username
                session["admin"] = user.admin
                session["user_id"] = user._id
                res = make_response(redirect(url_for('admin' if user.admin else 'home')))
                res.set_cookie('email', user.email)
                flash("You have been logged in.")
                return res
            flash("Email or Password not correct!")
        return render_template('login.html', form=form)

    return app


if __name__ == "__main__":
    MYAPP = create_app()
    MYAPP.run(debug=True, port=3000, host="0.0.0.0")
