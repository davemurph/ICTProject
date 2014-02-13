from flask.ext.wtf import Form
from wtforms import TextField, SubmitField, SelectField, validators, ValidationError
from rates import populateCurrencyList


class ConversionForm(Form):
	fromCurrency = SelectField('From currency:', choices=populateCurrencyList())
	toCurrency = SelectField('To currency:', choices=populateCurrencyList())

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