from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, DEFAULT_IMAGE_URL
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


@app.route("/users")
def list_users():
    """Shows list of all usesrs in db"""
    users = User.query.all()
    return render_template("list.html", users=users)


@app.route("/users/new")
def show_new_user_form():

    return render_template("form.html")


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
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)

@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first']
    user.last_name = request.form['last']
    if request.form['url']:
        user.image_url = request.form['url'] 
    else:
        user.image_url = DEFAULT_IMAGE_URL

  
    db.session.add(user)
    db.session.commit()
    
    return redirect("/users")
    
    
@app.route('/users/<int:user_id>/delete', methods = ["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    
    db.session.delete(user)
    db.session.commit()
    
    return redirect("/users")

