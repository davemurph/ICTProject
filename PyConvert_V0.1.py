# ICT Project 2014
# D Murphy
#
# PyConvert_V0.1

# imports
from flask import Flask, request, redirect, url_for, render_template
	
# configuration
DEBUG = True
SECRET_KEY = 'development key'

# hard-coded currency conversion rates
GBP_TO_EURO = 1.21

# create the application
app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def render_home():
	return render_template('base.html', rate=GBP_TO_EURO)

@app.route('/calculate', methods=['POST'])
def calculate_values():		
	try:
		amount_as_string = request.form['currency']
		amount = float(amount_as_string)
		converted_amount = GBP_TO_EURO * amount
		return render_template('conversion.html', input=amount, output=converted_amount, rate=GBP_TO_EURO)
	except ValueError:
		error = 'You must enter a numerical value! Try again.'
		return render_template('conversion.html', error=error, rate=GBP_TO_EURO)
	
@app.route('/clear', methods=['POST'])
def clear_conversion():
	return redirect(url_for('render_home'))
		
if __name__ == '__main__':
	app.run()