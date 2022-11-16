"""Seed file to make sample data for users db."""

from models import User, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

# If table isn't empty, empty it
User.query.delete()

# Add users
adam = User(first_name='Adam', last_name="Pecan")
freddie = User(first_name='Freddie', last_name="Walnut")
val = User(first_name='Val', last_name="Wild", image_url='https://cdn.hswstatic.com/gif/fractal-update1.jpg')

# Add new objects to session, so they'll persist
db.session.add(adam)
db.session.add(freddie)
db.session.add(val)

# Commit--otherwise, this never gets saved!
db.session.commit()