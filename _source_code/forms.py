# forms.py
# Input forms using Flask-WTF

# forms.py calls in to exchange_api to
# populate SelectFields with exchange rates

from flask import redirect, url_for
from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, SelectField, PasswordField, validators
from wtforms import ValidationError
from models import db, User
import json, requests
from configobj import ConfigObj
from werkzeug import generate_password_hash, check_password_hash


# config data
config = ConfigObj('config_settings_dev.ini')
api_loginuser_url = config['urls']['url_loginuser']
api_createuser_url = config['urls']['url_createuser']
api_queryuser_url = config['urls']['url_queryuser']
headers = {'Content-Type': 'application/json'}



class ConversionForm(Form):
	
	#currencies = populate_currencies()	
	
	fromCurrency = SelectField('From currency:', choices=())

	toCurrency =   SelectField('To currency:', choices=())

	conversionAmount = TextField('Enter amount to convert:', 
				[validators.Required('Please enter a conversion amount')])
	
	convertButton = SubmitField('Convert')
		
	def validate(self):
		if not Form.validate(self):
			return False
	
		try:
			amount = float(self.conversionAmount.data)
			return True
		except ValueError:
			self.conversionAmount.errors.append('You must enter a numerical value! Try again.')
			return False
	
	
class EnterForm(Form):
	enterButton = SubmitField('Try A Conversion!')


class JoinUsForm(Form):
	email = TextField('Email', [validators.Required('You must supply an email address'), validators.Email('The email address you supplied is not valid')])
	password = PasswordField('Password', [validators.Required("You must supply a password")])
	submit = SubmitField('Create user account')

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
		
		request_parameters = {'email': self.email.data}
		json_request_parameters = json.dumps(request_parameters)
		json_response = requests.post(api_queryuser_url, 
									  data = json_request_parameters, 
									  headers = headers)

		if json_response.status_code != 200:
			response_code = json_response.status_code
			raise LoginUserException()
					
		user_query = json_response.json()

		if user_query['user_exists'] == 'true':
			self.email.errors.append('That email address already exists')
			return False
		else:			
			return True


class LoginForm(Form):
	email = TextField('Email',  [validators.Required('You must supply an email address.'), validators.Email('The email address you supplied is not valid')])
	password = PasswordField('Password', [validators.Required('You must supply a password.')])
	submit = SubmitField('Log In')
   
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
 
	def validate(self):
		if not Form.validate(self):
			return False

		request_parameters = {'email': self.email.data, 'password': self.password.data}
		json_request_parameters = json.dumps(request_parameters)
		json_response = requests.post(api_queryuser_url, 
									  data = json_request_parameters, 
									  headers = headers)

		if json_response.status_code != 200:
			response_code = json_response.status_code
			raise LoginUserException()
					
		user_query = json_response.json()

		if user_query['user_exists'] == 'true':			
			return True
		else:
			self.email.errors.append('Invalid e-mail address or password')			
			return False
		

class LoginUserException(Exception):
	pass