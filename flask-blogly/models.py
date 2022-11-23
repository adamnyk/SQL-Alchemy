"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref
from sqlalchemy.sql import func

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://cdn-icons-png.flaticon.com/512/149/149071.png"


def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW!
class User(db.Model):
    __tablename__ = "users"

    def __repr__(self):
        return f"<User {self.id} {self.first_name} {self.last_name} {self.image_url}>"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # TODO: Figure out how to make first+last unique.
    first_name = db.Column(db.Text, nullable=False)
    last_name = db.Column(db.Text, nullable=False)
    image_url = db.Column(db.Text, nullable=False, default=DEFAULT_IMAGE_URL)

    @property
    def full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    __tablename__ = "posts"

    def __repr__(self):
        return (
            f"<Post {self.id} {self.title} {self.created_at} User_id: {self.user_id}>"
        )

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=func.now(),
        # Line below is to update when edited
        # onupdate=func.now()
    )
    user_id = db.Column(
        db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    user = db.relationship("User", backref=backref("posts", passive_deletes="all"))
    tags = db.relationship("Tag", secondary="posts_tags", backref="posts")

    @property
    def friendly_date(self):
        """Return readable version of date"""
        return self.created_at.strftime("%b. %-d, %Y - %-I:%M %p")


class Tag(db.Model):
    """Descriptive tags for user posts."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)


    def __repr__(self):
        return (f"<Tag: {self.id} {self.name}>")

class PostTag(db.Model):
    """Mapping of a post to a tag."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

