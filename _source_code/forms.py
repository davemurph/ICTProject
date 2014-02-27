# forms.py
# Input forms using Flask-WTF

# forms.py calls in to exchange_api to
# populate SelectFields with exchange rates

from flask import flash, url_for, redirect
from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, SelectField, validators, ValidationError 
import json, requests


# set up dummy user for authentication, to match authenticated
# user in exchange_api
user = ('daithi', 'pass1234')


# assign URL's for exchange_api
api_getcurrencies_url = 'http://localhost:8000/testapi/getcurrencies'


# define headers for JSON data
headers = {'Content-Type': 'application/json'}

def populate_currencies():
	# populate currency SelectFields with currencies in exchange_api
	# must check response code prior to populating
	json_currencies = requests.get(api_getcurrencies_url, headers=headers, auth=user)
	if json_currencies.status_code == 403:
		flash('You are not an authorised user')
		return redirect(url_for('home'))
	elif json_currencies.status_code != 200:
		flash('There is a problem accessing the api')
		return redirect(url_for('home'))
	else:
		currencies = json_currencies.json()
		return currencies

class ConversionForm(Form):
	
	currencies = populate_currencies()	
	
	fromCurrency = SelectField('From currency:', choices=currencies['currency_list'])
	toCurrency = SelectField('To currency:', choices=currencies['currency_list'])

	conversionAmount = TextField("Enter amount to convert:", [validators.Required("Please enter a conversion amount")])
	convertButton = SubmitField("Convert")
		
	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)
	
	def validate(self):
		if not Form.validate(self):
			return False
	
		try:
			amount = float(self.conversionAmount.data)
			return True
		except ValueError:
			self.conversionAmount.errors.append('You must enter a numerical value! Try again.')
			return False
	
	
class ResultForm(Form):
	clearButton = SubmitField("Another conversion")
	
	
class EnterForm(Form):
	enterButton = SubmitField("Try A Conversion!")
