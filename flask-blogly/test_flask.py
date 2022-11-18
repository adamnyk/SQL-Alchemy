from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    '''Tests for views of Users.'''
    
    def setUp(self):
        '''Clear all users and add a sample user'''
        User.query.delete()
        
        user = User(first_name="Test", last_name="Dummy", image_url="https://imageio.forbes.com/specials-images/imageserve/513343414/960x0.jpg?format=jpg&width=960")
        
        db.session.add(user)
        db.session.commit()

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
        
    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test Dummy', html)
            
    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/1")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Test Dummy</h1>', html)
            self.assertIn('Edit</a>', html)
            self.assertIn('https://imageio.forbes.com/specials-images/imageserve/513343414/960x0.jpg', html)
            
    def test_add_user(self):
        with app.test_client() as client:
            d = {"first": "Eddie", "last": "Walnut", "url":""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Eddie Walnut</a></li>", html)
            
    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/1/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('Test Dummy', html)
