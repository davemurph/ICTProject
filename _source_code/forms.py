# forms.py
# Input forms using Flask-WTF

# forms.py calls in to exchange_api to
# populate SelectFields with exchange rates

from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, SelectField, validators
from wtforms import ValidationError 


class ConversionForm(Form):
	
	#currencies = populate_currencies()	
	
	fromCurrency = SelectField('From currency:', choices=())

	toCurrency =   SelectField('To currency:', choices=())

	conversionAmount = TextField("Enter amount to convert:", 
				[validators.Required("Please enter a conversion amount")])
	
	convertButton = SubmitField("Convert")
		
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
