# forms.py
# Input forms using Flask-WTF

# forms.py calls in to exchange_api to
# populate SelectFields with exchange rates

from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, SelectField, PasswordField, validators
from wtforms import ValidationError
from models import db, User


class ConversionForm(Form):
	
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
	password_confirm = PasswordField('Confirm password')
	submit = SubmitField('Create user account')

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False

		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user:
			self.email.errors.append('That email is in use. Try again.')
			return False
		elif self.password.data != self.password_confirm.data:
			self.password.errors.append('Passwords do not match. Try again.')
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
     
		user = User.query.filter_by(email = self.email.data.lower()).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.email.errors.append('Invalid e-mail address or password')
		return False