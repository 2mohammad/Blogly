from flask import Flask, request, render_template, redirect, flash, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Blog, Posts, Tag, PostTag

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
    tags = Tag.query.all()
    return render_template('make_post.html', user=user, tags=tags)

@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def add_posts_redirect(user_id):
    user_id = user_id
    title = request.form["inputTitle"]
    content = request.form["inputContent"]
    print(request.form.getlist('tag_names'))
    tag_list = request.form.getlist('tag_names')
    new_post = Posts(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()
    new_post = new_post.id
    for tag in tag_list:
        new_post_tag = PostTag(post_id=new_post, tag_id=tag)
        db.session.add(new_post_tag)

    db.session.commit()
    return redirect(f'/users/{user_id}')
    #return render_template('tags_temp.html', tag_list=tag_list)
    
@app.route('/posts/<int:post_id>')
def view_post(post_id):
    post = Posts.query.get_or_404(post_id)
    user = Posts.get_post_maker(post_id)
    tags = post.tags
    for tag in tags:
        print(tag.name)
    return render_template('post.html', post=post, user=user, tags=tags)

@app.route('/posts/<int:post_id>/delete')
def delete_post(post_id):
    post = Posts.query.get_or_404(post_id)
    tags = post.post_and_tags
    for tag in tags:
        db.session.delete(tag)
    db.session.delete(post)
    user = Posts.get_post_maker(post_id)
    userID = user['id']
    db.session.commit()
    return redirect(f'/users/{userID}')

@app.route('/posts/<int:post_id>/edit')
def edit_post_view(post_id):
    post = Posts.query.get_or_404(post_id)
    user = Posts.get_post_maker(post_id)
    post_tags = post.tags
    all_tags = Tag.query.all()
    tags = []
    tagged = []
    for tag in all_tags:
        tags.append(tag.id)
    for tag in post_tags:
        tagged.append(tag.id)

    xtags = [x for x in tags if x not in tagged]

    return render_template('edit_post.html', post=post, user=user, post_tags=post_tags, all_tags=all_tags, tags=tags, xtags=xtags)

@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def edit_post_submit(post_id):
    post = Posts.query.get_or_404(post_id)
    post.title = request.form["inputTitle"]
    post.content = request.form["inputContent"]
    tags = post.post_and_tags
    for tag in tags:
        db.session.delete(tag)
    tag_list = request.form.getlist('tag_names')
    for tag in tag_list:
        tagId = Tag.query.get_or_404(tag)
        new_post_tag = PostTag(post_id=post.id, tag_id=tagId.id)
        db.session.add(new_post_tag)

    db.session.commit()

    return redirect(f'/posts/{post.id}')

@app.route('/tags/new')
def make_tag():
    return render_template('make_tags.html')

@app.route('/tags', methods=["POST"])
def add_tag():
    name = request.form["inputTagName"]
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags')
def show_tags():
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    tag_posts = Tag.query.get_or_404(tag_id).post
    tag = Tag.query.get_or_404(tag_id)
    return render_template('show_tag.html', tag_posts=tag_posts, tag=tag)
