# ICT Project 2014
# D Murphy
#
# rates.py

# functions to perform conversion calculations
# with data retrieved from exchange_api

####################################
####  NOT USED (04 March 2014)  ####
####################################

import json, requests
from requests.auth import HTTPBasicAuth

# assign URL's for exchange_api
api_convert_url = 'http://localhost:8000/testapi/convert'


# define headers for JSON data
headers = {'Content-Type': 'application/json'}


def convert_currency(user, from_currency, to_currency, amount):
		
	# define parameters for HTTP POST request to exchange_api
	request_params = {'from_currency': from_currency,
					'to_currency': to_currency,
					'amount': amount}
	
	# encode parameters as JSON
	json_request_params =  json.dumps(request_params)
	
	# POST to exchange_api with parameters and 
	json_response = requests.post(api_convert_url, json_request_params, 
									headers=headers, auth=user)
		
	# decode JSON response
	result = json_response.json()	
	
	# convert response values to formatted strings for presentation
	converted_amount = '%.2f' % result['converted_amount']
	unit_rate = '%.5f' % result['unit_rate']
	
	return {'converted_amount': converted_amount, 'unit_rate': unit_rate}
			
