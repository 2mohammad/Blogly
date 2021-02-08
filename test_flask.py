from app import app
from models import db, Blog
from unittest import TestCase

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False
# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()



 

class FlaskTests(TestCase):
    def create(self):
        self.client = app.test_client()

    def setUp(self):
        """Add sample pet."""

        Blog.query.delete()

        user = Blog(first_name="TestFirstName12334", last_name="TestLastName", image_url="www.www.com")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id


    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()
    def test_users_route(self):
        with app.test_client() as client:
            response = client.get('/users')
            html = response.get_data(as_text=True)

            self.assertIn("TestFirstName", html)
            self.assertEqual(response.status_code, 200)
        

    def test_create_users_route(self):
        with app.test_client() as client:
            response = client.get('/users/new')
            html = response.get_data(as_text=True)
            user = Blog(first_name="TestFirstName", last_name="TestLastName", image_url="www.www.com")
            db.session.add(user)
            self.assertIn("First Name", html)
            self.assertEqual(response.status_code, 200)
    
    def test_details_route(self):
        with app.test_client() as client:
            response = client.get(f'/users/{self.user_id}')
            html = response.get_data(as_text=True)
            self.assertIn("TestFirstName12334 TestLastName", html)
            self.assertEqual(response.status_code, 200)
    
    def test_detailss_route(self):
        with app.test_client() as client:
            #dat = dict(inputFirstName="TestFirstName12334s", inputLasttName="TestLastNsame", inputURL="wsww.www.com")
            dat = {"inputFirstName": "TestPet2", "inputLastName": "cat", "inputURL": "www.adaddada.com"}

            client.post('/users/new', data=dat, follow_redirects=True)
            response = client.get('/users')
            html = response.get_data(as_text=True)
            print(html)
            self.assertIn("TestPet2", html)
            self.assertEqual(response.status_code, 200)
