# RESTful api (Flask/Python)

# currency conversion
# all data in HTTP methods is JSON format

# getSpecificRate() and exchange() return floats
# getRate() returns a float

# get_active_currency_list() returns currency
# dictionary (JSON format)

# exchange rates are relative to 1.0 * Euro

# code structure adapted from tutorial at 
# http://blog.miguelgrinberg.com/post/designing-a-restful-api-with-python-and-flask
# by Miguel Grinberg


from flask import Flask, jsonify, abort, request, make_response
from flask.ext.httpauth import HTTPBasicAuth
import json, requests, threading, time


app = Flask(__name__)
auth = HTTPBasicAuth()


# hard-coded exchange rates
#exchange_rates = 	{'EUR': 1.0, 
#					'USD': 1.36379, 
#					'GBP': 0.82910, 
#					'AUD': 1.51202, 
#					'CAD': 1.50140, 
#					'NZD': 1.64072}


# define global variable exchange_rates, with value of 'EUR' = 1.0
# all rates are relative to 1.0 Euro
exchange_rates = {'EUR': 1.0}


# function to get live rates periodically, runs on seperate thread
def get_live_rates():	
	while True:
		# json feed with live currency rates
		json_live_rates = requests.get('http://spreadsheets.google.com/feeds/list/0Av2v4lMxiJ1AdE9laEZJdzhmMzdmcW90VWNfUTYtM2c/3/public/basic?alt=json')
		live_rates = json_live_rates.json()
	
		global exchange_rate_last_update
		exchange_rate_last_update = time.ctime()
	
		# populate dict with downloaded currency rates	
		for i in range(9):
			currency = 	live_rates['feed']['entry'][i]['title']['$t']
			rate_as_string = live_rates['feed']['entry'][i]['content']['$t']
			rate = float(rate_as_string[8:])
			exchange_rates[currency] = rate		
	
		time.sleep(10)
	

# start get_live_rates thread	
rates_thread = threading.Thread(target=get_live_rates)
rates_thread.daemon = True # allows keyboard interrupt (ctrl-c) of all threads
rates_thread.start()
					

# user authorisation
@auth.get_password
def get_password(username):
	if username == 'daithi':
		return 'pass1234'
	return None


@auth.error_handler
def unauthorized():
	return make_response(jsonify( { 'error': 'Unauthorised access' } ), 403)
	

# url to return specific exchange rate
@app.route('/testapi/convert/<string:currency>', methods = ['GET'])
#@auth.login_required
def get_rate(currency):
	if currency in exchange_rates:
		return jsonify ( { 'rate': exchange_rates[currency] } )
	else:
		abort(404)
		
	
# url to return currency conversion based on JSON request parameters		
@app.route('/testapi/convert', methods = ['POST'])
@auth.login_required
def convert_amount():
	if not request.json:
		abort(400)
	if not 'from_currency' in request.json:
		abort(400)
	if not 'to_currency' in request.json:
		abort(400)
	if not 'amount' in request.json:
		abort(400)
		
	if not validate_amount(request.json['amount']):
		abort(400)
		
	if request.json['from_currency'] not in exchange_rates:
		abort(404)
	if request.json['to_currency'] not in exchange_rates:
		abort(404)

	converted_amount = exchange(request.json['from_currency'], 
						request.json['to_currency'], 
						request.json['amount'])

	specific_rate = get_unit_rate(request.json['from_currency'],
									request.json['to_currency'])

	return jsonify( { 'converted_amount': converted_amount, 
						'unit_rate': specific_rate, 'last_update': exchange_rate_last_update } )


# url to return dictionary of currencies in JSON
@app.route('/testapi/getcurrencies', methods = ['GET'])
@auth.login_required
def get_active_currency_list():
	currency_list = []
	for currency in exchange_rates:
		currency_list.append((currency, currency))
		
	return jsonify ( { 'currency_list': currency_list } )


# JSON error handlers
@app.errorhandler(404)
def not_found(error):
		return make_response(jsonify( { 'error': 'Resource not found' } ), 404)
		
		
@app.errorhandler(400)
def bad_request(error):
		return make_response(jsonify( { 'error': 'Bad request' } ), 400)
		

# utility methods
def get_unit_rate(from_currency, to_currency):
	from_rate = exchange_rates[from_currency]		
	to_rate = exchange_rates[to_currency]
		
	return to_rate / from_rate
	
			
def exchange(from_currency, to_currency, amount):
	from_rate = exchange_rates[from_currency]		
	to_rate = exchange_rates[to_currency]
		
	return amount * to_rate / from_rate
	
	
def validate_amount(amount):
	if isinstance(amount, basestring):
		return False	
	else:
		try:
			float(amount)
			return True
		except ValueError:
			return False


# execute api on port 8000
if __name__ == '__main__':
	app.run(debug = True, port = 8000)
