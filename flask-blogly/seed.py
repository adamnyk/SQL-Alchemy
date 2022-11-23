"""Seed file to make sample data for users db."""

from models import User, Post, db, Tag, PostTag
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
adam = User(first_name="Adam", last_name="Pecan")
eddie = User(
    first_name="Eddie",
    last_name="Walnut",
    image_url="https://indianmemetemplates.com/wp-content/uploads/Imagination-Spongebob.jpg",
)
val = User(
    first_name="Val",
    last_name="Wild",
    image_url="https://cdn.hswstatic.com/gif/fractal-update1.jpg",
)
caro = User(
    first_name="Caro",
    last_name="TrundleDove",
    image_url="https://www.rainforest-alliance.org/wp-content/uploads/2021/06/three-toed-sloth-teaser-1.jpg.optimal.jpg",
)


# Add new objects to session, so they'll persist
db.session.add(adam)
db.session.add(eddie)
db.session.add(val)
db.session.add(caro)

# Commit--otherwise, this never gets saved!
db.session.commit()

jazz = Post(
    title="JazzMattaz",
    content="Jazz is the best and a truly American art form! Check out kuvo.org community radio station for incredible music, culture, and community in the Denver area.",
    user_id="1",
)
swing = Post(
    title="It don" "t mean a thing...",
    content=".... if you ain" "t got that swing! Do wap do wap!",
    user_id="2",
)
cacao = Post(
    title="Cacao and stuff",
    content="blah, blah, blah. Cacao tastes great!",
    user_id="3",
)
eat = Post(
    title="Things I like to eat....",
    content="I like to eat leaves, hibiscus flowers, and Starburst jellybeans!!!!",
    user_id="4",
)


db.session.add(jazz)
db.session.add(swing)
db.session.add(cacao)
db.session.add(eat)

db.session.commit()
