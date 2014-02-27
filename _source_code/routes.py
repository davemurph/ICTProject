# ICT Project 2014
# D Murphy
#
# routes.py

# imports
from _source_code import app
from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
from forms import ConversionForm, ResultForm, EnterForm
import json, requests
from requests.auth import HTTPBasicAuth


# set up dummy user for authentication, to match authenticated
# user in exchange_api
user = ('daithi', 'pass1234')

# assign URL's for exchange_api
api_convert_url = 'http://localhost:8000/testapi/convert'

# define headers for JSON data
headers = {'Content-Type': 'application/json'}


@app.route('/', methods=['GET', 'POST'])
def home():
	form = EnterForm()
		
	if request.method == 'POST':
		return redirect(url_for('conversion'))
	
	elif request.method == 'GET':
		return render_template('home.html', form=form)


@app.route('/convert', methods=['GET', 'POST'])
def conversion():		
	form = ConversionForm()
	
	if request.method == 'POST':
		if form.validate() == False:
			form.conversionAmount.data = ''
			return render_template('conversion.html', form=form)
		else:
			# get input values
			from_currency = form.fromCurrency.data
			to_currency = form.toCurrency.data	
			amount = float(form.conversionAmount.data)
			
			# define parameters for HTTP POST request to exchange_api
			request_params = {'from_currency': from_currency,
								'to_currency': to_currency,
								'amount': amount}
								
			# encode parameters as JSON
			json_request_params =  json.dumps(request_params)
			
			# POST to exchange_api with parameters and 
			json_response = requests.post(api_convert_url, json_request_params, 
											headers=headers, auth=user)
			
			# check HTTP response code
			if json_response.status_code == 403:
				return render_template('unauthorised.html')
			else:
				# decode JSON response
				result = json_response.json()
				
				# convert response values to formatted strings for presentation
				converted_amount = '%.2f' % result['converted_amount']
				unit_rate = '%.5f' % result['unit_rate']
				formatted_amount = '%.2f' % (amount)
				last_update = result['last_update']
		
			return render_template('conversion.html', form=form, input_amount=formatted_amount, 
				from_currency=from_currency, to_currency=to_currency, 
				converted_amount=converted_amount, unit_rate=unit_rate, last_update=last_update)

	elif request.method == 'GET':		
		return render_template('conversion.html', form=form)
