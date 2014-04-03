from flask.ext.testing import TestCase
import unittest
from _source_code import app
from _source_code.models import db, User
from _source_code.routes import round_to_two_places, round_to_six_places
from decimal import Decimal


class TestClientWithUser(TestCase):

	# config testing environment, db etc.
	def create_app(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		return app

	def setUp(self):
		db.create_all()
		self.create_user('test1@test.com', 'pass1234')

	def tearDown(self):
		db.session.remove()
		db.drop_all()

	# some helper methods to assist testing methods
	def login_user(self, email, password):
		return self.client.post('/login', data = dict(email = email, password = password), follow_redirects = True)

	def logout_user(self):
		return self.client.get('/logout', follow_redirects=True)

	def post_conversion_values(self, from_currency, to_currency, amount):		
		return self.client.post('/convert',
								data = dict(fromCurrency = from_currency, toCurrency = to_currency, conversionAmount = amount), 
								follow_redirects = True)

	def post_new_user_details(self, email, password, password_confirm):
		return self.client.post('/joinus',
								data = dict(email = email, password = password, password_confirm = password_confirm),
								follow_redirects = True)

	def create_user(self, email, password):
		user = User(email, password)
		db.session.add(user)
		db.session.commit()


	# testing methods
	def test_user_login_logout(self):
		valid_login = self.login_user('test1@test.com', 'pass1234')
		assert 'logged in as' in valid_login.data

		logged_out = self.logout_user()
		assert 'logged in as' not in logged_out.data

		invalid_login1 = self.login_user('invalid@email.com', 'invalidPassword')
		assert 'Invalid e-mail address or password' in invalid_login1.data
		
		invalid_login2 = self.login_user('test1@test.com', 'invalidPassword')
		assert 'Invalid e-mail address or password' in invalid_login2.data


	def test_create_new_user(self):
		response_invalid_email = self.post_new_user_details('bad_email_format', 'pass1234', 'pass1234')
		assert 'The email address you supplied is not valid' in response_invalid_email.data

		response_no_email = self.post_new_user_details('', 'pass1234', 'pass1234')
		assert 'You must supply an email address' in response_no_email.data

		response_no_password_supplied = self.post_new_user_details('test2@test.com', '', '')
		assert 'You must supply a password' in response_no_password_supplied.data

		response_passwords_not_match = self.post_new_user_details('test2@test.com', 'pass1234', 'xyz')
		assert 'Passwords do not match. Try again.' in response_passwords_not_match.data

		response_username_exists = self.post_new_user_details('test1@test.com', 'pass1234', 'pass1234')
		assert 'That email is in use. Try again.' in response_username_exists.data


	def test_route_convert(self):
		self.login_user('test1@test.com', 'pass1234')

		response_get_convert_page = self.client.get('/convert')
		assert 'Select from currencies' in response_get_convert_page.data

		response_post_valid_data = self.post_conversion_values('EUR', 'GBP', '123.45')
		assert 'Currency rates last updated' in response_post_valid_data.data

		response_post_invalid_amount = self.post_conversion_values('EUR', 'USD', 'xyz')
		assert 'You must enter a numerical value!' in response_post_invalid_amount.data

		response_post_negative_amount = self.post_conversion_values('GBP', 'CAD', '-23.54')
		assert 'You cannot enter a negative number' in response_post_negative_amount.data



class TestClientFunctions(TestCase):

	# config testing environment, db etc.
	def create_app(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		return app


	def test_round_to_two_places(self):
		rounded_number = round_to_two_places(123.45678)
		self.assertEqual(rounded_number, Decimal('123.46'))

	def test_round_to_six_places(self):
		rounded_number = round_to_six_places(347.1242798201)
		self.assertEqual(rounded_number, Decimal('347.124280'))

class TestRoutes(TestCase):
	# config testing environment, db etc.
	def create_app(self):
		app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite://'
		app.config['TESTING'] = True
		app.config['WTF_CSRF_ENABLED'] = False
		return app

	render_templates = False


	def test_home_page_route(self):
		response_home_page = self.client.get('/')
		#self.assert200(response_home_page)
		assert "" == response_home_page.data
		self.assert_template_used('home.html')
	

	#def test_
