from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Blog, Posts

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "oh-so-secret"
debug = DebugToolbarExtension(app)
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)

@app.route('/users/new')
def show_form():
    return render_template('add_users.html')

@app.route('/users/new', methods=["POST"])
def add_user():
    print(request.form)
    first_name =  request.form["inputFirstName"]
    last_name = request.form["inputLastName"]
    image_url = request.form["inputURL"]
    new_user = Blog(first_name=first_name, last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users')
def users_list():
    user_list = Blog.query.all()
    return render_template('user_list.html', user_list=user_list)

@app.route('/users/<int:user_id>')
def show_user(user_id):
    user = Blog.query.get_or_404(user_id)
    posts = Posts.query.filter(Posts.user_id == user_id)
    return render_template('details.html', user=user, posts=posts)

@app.route('/users/<int:user_id>/delete')
def remove_user(user_id):
    user = Blog.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/edit')
def edit_user(user_id):
    user = Blog.query.get_or_404(user_id)
    return render_template('edit.html', user=user)

@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user_form(user_id):
    first_name =  request.form["inputFirstName"]
    last_name = request.form["inputLastName"]
    image_url = request.form["inputURL"]
    user = Blog.query.get_or_404(user_id)
    user.first_name = first_name
    user.last_name = last_name
    user.image_url = image_url
    db.session.commit()
    return redirect('/users')

@app.route('/users/<int:user_id>/posts/new')
def add_posts(user_id):
    user = Blog.query.get_or_404(user_id)
    return render_template('make_post.html', user=user)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_posts_redirect(user_id):
    user_id = user_id
    title = request.form["inputTitle"]
    content = request.form["inputContent"]
    new_post = Posts(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/posts/<int:post_id>')
def view_post(post_id):
    post = Posts.query.get_or_404(post_id)
    user = Posts.get_post_maker(post_id)
    return render_template('post.html', post=post, user=user)

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    user = Posts.get_post_maker(post_id)
    userID = user['id']
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{userID}')

@app.route('/posts/<int:post_id>/edit')
def edit_post_view(post_id):
    post = Posts.query.get_or_404(post_id)
    user = Posts.get_post_maker(post_id)
    return render_template('edit_post.html', post=post, user=user)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_submit(post_id):
    post = Posts.query.get_or_404(post_id)
    post.title = request.form["inputTitle"]
    post.content = request.form["inputContent"]
    db.session.commit()
    return redirect(f'/posts/{post.id}')
