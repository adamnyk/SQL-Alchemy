from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, DEFAULT_IMAGE_URL, Post, Tag, PostTag

# from seed import *

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "chickenzarecool21837"
app.config["DEBUG_TB_INTERCEPT_REDIRECTS"] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

# Add sample data to database
# exec(open("./seed.py").read())


@app.route("/")
def home():
    """Redirect to users list"""
    return redirect("/users")


##################################################
# User route


@app.route("/users")
def list_users():
    """Shows list of all usesrs in db"""
    users = User.query.all()
    return render_template("users/list.html", users=users)


@app.route("/users/new")
def show_new_user_form():

    return render_template("users/form.html")


@app.route("/users/new", methods=["POST"])
def add_user():
    """Add user to db and redirect to list"""

    first = request.form["first"]
    last = request.form["last"]
    url = request.form["url"]

    user = User(first_name=first, last_name=last, image_url=url or None)
    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show user page and their posts"""
    user = User.query.get_or_404(user_id)
    posts = Post.query.filter(Post.user_id == user_id).all()

    return render_template("users/details.html", user=user, posts=posts)


@app.route("/users/<int:user_id>/edit")
def show_edit_user_form(user_id):
    """Show form to edit user profile."""
    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)


@app.route("/users/<int:user_id>/edit", methods=["POST"])
def edit_user(user_id):
    """Submit changes to edit user profile"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first"]
    user.last_name = request.form["last"]
    if request.form["url"]:
        user.image_url = request.form["url"]
    else:
        user.image_url = DEFAULT_IMAGE_URL

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/delete", methods=["POST"])
def delete_user(user_id):
    """Delete user"""
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


################################################
# Posts route


@app.route("/users/<int:user_id>/posts/new")
def new_post_form(user_id):
    """Show new post form"""
    user = user = User.query.get_or_404(user_id)

    return render_template("posts/new.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=["POST"])
def submit_new_post(user_id):
    """Handle new post submission"""
    title = request.form["title"]
    content = request.form["content"]

    new_post = Post(title=title, content=content, user_id=user_id)

    db.session.add(new_post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def show_post(post_id):
    """Show post information"""
    post = Post.query.get_or_404(post_id)
    return render_template("posts/view.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def posts_edit_form(post_id):
    # '''Show a form to exit existing post'''
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template("posts/edit.html", post=post, tags=tags)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def posts_update(post_id):
    """Handle form submission for post update"""

    post = Post.query.get_or_404(post_id)

    post.title = request.form["title"]
    post.content = request.form["content"]
    
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{post.user_id}")


@app.route("/posts/<int:post_id>/delete", methods=["POST"])
def delete_post(post_id):
    """Handle delete post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()

    return redirect("/users")


##########################################################
# Tag routes


@app.route("/tags")
def list_tags():
    """Show list of all tags."""

    tags = Tag.query.all()
    return render_template("tags/list.html", tags=tags)


@app.route("/tags/new")
def new_tag():
    """Show form to add a new tag."""
    posts = Post.query.all()
    return render_template("tags/new.html", posts=posts)


@app.route("/tags/new", methods=["POST"])
def handle_new_tag():
    """Handle new tag submission."""

    post_ids = [int(num) for num in request.form.getlist("posts")]
    posts = Post.query.filter(Post.id.in_(post_ids)).all()
    new_tag = Tag(name=request.form["name"], posts=posts)

    db.session.add(new_tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def show_tag(tag_id):
    """Show tag posts."""
    tag = Tag.query.get_or_404(tag_id)
    return render_template("tags/details.html", tag=tag)


@app.route("/tags/<int:tag_id>/edit")
def edit_tag_form(tag_id):
    """Show form to edit tag"""
    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()

    return render_template("tags/edit.html", tag=tag, posts=posts)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def handle_edit_tag(tag_id):
    """Handle edit tag form submission."""

    tag = Tag.query.get_or_404(tag_id)

    tag.name = request.form["name"]
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()

    return redirect("/tags")


@app.route("/tags/<int:tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete tag from database."""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")
