# ICT Project 2014
# D Murphy
#
# routes.py

from _source_code import app
from flask import Flask, request, redirect, url_for, render_template, flash, jsonify
from forms import ConversionForm, ResultForm, EnterForm
from currencies import Currencies
import json, requests
from decimal import Decimal

user = ('daithi', 'pass1234') # dummy user for exchange_api

api_convert_url = 'http://localhost:8000/testapi/convert'

headers = {'Content-Type': 'application/json'}


@app.route('/', methods=['GET', 'POST'])
def home():
	form = EnterForm()
		
	if request.method == 'POST':
		return redirect(url_for('convert'))
	
	elif request.method == 'GET':
		return render_template('home.html', form=form)


@app.route('/convert', methods=['GET', 'POST'])
def convert():	
	currency_feed = Currencies()

	currency_feed.test_feed_connection()

	if currency_feed.request_status_code == 200: # case connection succeeded
		form = ConversionForm()
		
		currency_dict = currency_feed.get_currency_list()['currency_list']

		currency_code_list = []
		for currency_code in currency_dict:
			currency_code_list.append((currency_code, currency_code + ' - ' + currency_dict[currency_code]))

		form.fromCurrency.choices = currency_code_list
		form.toCurrency.choices = currency_code_list

		if request.method == 'GET':		
			return render_template('conversion.html', form=form)

		elif request.method == 'POST':
			if form.validate() == False:
				form.conversionAmount.data = ''
				return render_template('conversion.html', form=form)

			else:
				from_currency = form.fromCurrency.data
				from_currency_label = currency_dict[from_currency]

				to_currency = 	form.toCurrency.data
				to_currency_label = currency_dict[to_currency]

				amount = 		form.conversionAmount.data
			
				request_parameters = {'from_currency': from_currency,
									  'to_currency': to_currency,
									  'amount': amount}

				json_request_parameters = json.dumps(request_parameters)
			
				json_response = requests.post(api_convert_url, 
											  json_request_parameters, 
											  headers=headers, 
											  auth=user)

				if json_response.status_code == 403:
					return redirect(url_for('unauthorised'))
				
				else:
					result = json_response.json()
				
					converted_amount = round_to_two_places(result['converted_amount'])
					unit_rate = 	   round_to_six_places(result['unit_rate'])
					formatted_amount = round_to_two_places(amount)
					last_update = 	   result['last_update']

		
					return render_template('conversion.html', 
											form = form, 
											input_amount = formatted_amount, 
											from_currency = from_currency,
											from_currency_label = from_currency_label,
											to_currency = to_currency, 
											to_currency_label = to_currency_label,
											converted_amount = converted_amount, 
											unit_rate = unit_rate, 
											last_update = last_update)

	else: # case connection failed
		if currency_feed.request_status_code == 403:
			return redirect(url_for('unauthorised'))

		elif currency_feed.request_status_code == 404:
			return redirect(url_for('unavailable'))

		elif currency_feed.request_status_code == 'connection_error':
			return redirect(url_for('unavailable'))


@app.route('/unauthorised')
def unauthorised():
	return render_template('unauthorised.html')


@app.route('/unavailable')
def unavailable():
	return render_template('api_unavailable.html')


def round_to_two_places(amount):
	TWOPLACES = Decimal('.01')
	return Decimal(amount).quantize(TWOPLACES)


def round_to_six_places(amount):
	FIVEPLACES = Decimal('.000001')
	return Decimal(amount).quantize(FIVEPLACES)