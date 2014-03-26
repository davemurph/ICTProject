# ICT Project 2014
# D Murphy
#
# routes.py

from _source_code import app
from flask import Flask, request, redirect, url_for, render_template, jsonify, session
from forms import ConversionForm, EnterForm, JoinUsForm, LoginForm
import json, requests
from decimal import Decimal
from configobj import ConfigObj
from models import db, User


# config data
config = ConfigObj('config_settings_dev.ini')
user = (config['userinfo']['username'], config['userinfo']['password'])
api_getcurrencies_url = config['urls']['url_getcurrencies']
api_convert_url = config['urls']['url_convert']
headers = {'Content-Type': 'application/json'}


@app.route('/', methods=['GET', 'POST'])
def home():
	form = EnterForm()
		
	if request.method == 'POST':
		return redirect(url_for('convert'))
	
	elif request.method == 'GET':
		return render_template('home.html', form=form)


@app.route('/joinus', methods=['GET', 'POST'])
def joinus():
	form = JoinUsForm()

	if 'email' in session:
		return redirect(url_for('home'))

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('joinus.html', form=form)
		else:
			newuser = User(form.email.data, form.password.data)
			db.session.add(newuser)
			db.session.commit()

			session['email'] = newuser.email
			return redirect(url_for('home'))

	elif request.method == 'GET':
		return render_template('joinus.html', form = form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
	form = LoginForm()

	if 'email' in session:
		return redirect(url_for('home'))

	if request.method == 'POST':
		if form.validate() == False:
			return render_template('login.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('home'))

	elif request.method == 'GET':
		return render_template('login.html', form = form)


@app.route('/logout')
def logout(): 
  if 'email' not in session:
    return redirect(url_for('login'))
     
  session.pop('email', None)
  return redirect(url_for('home'))


@app.route('/convert', methods=['GET', 'POST'])
def convert():
	if 'email' not in session:
		return redirect(url_for('login'))

	user_in_session = User.query.filter_by(email = session['email']).first()

	if user_in_session is None:
		return redirect(url_for('home'))
	else:
		try:
			form = ConversionForm()
		
			json_currency_request = requests.get(api_getcurrencies_url, 
												 headers=headers, 
												 auth=user)

			if json_currency_request.status_code != 200:
				response_code = json_currency_request.status_code
				raise CurrencyFeedException()

			currency_dict = json_currency_request.json()['currency_list']

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

					to_currency = form.toCurrency.data
					to_currency_label = currency_dict[to_currency]

					amount = form.conversionAmount.data
			
					request_parameters = {'from_currency': from_currency,
										  'to_currency': to_currency,
										  'amount': amount}

					json_request_parameters = json.dumps(request_parameters)
			
					json_response = requests.post(api_convert_url, 
											 	 json_request_parameters, 
											 	 headers=headers, 
											 	 auth=user)

					if json_response.status_code != 200:
						response_code = json_response.status_code
						raise CurrencyFeedException()				

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
		except CurrencyFeedException:
			if response_code == 403:
				return redirect(url_for('unauthorised'))

			elif response_code == 404:
				return redirect(url_for('unavailable'))

			elif response_code == 503:
				return redirect(url_for('unavailable'))

			else:
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

class CurrencyFeedException(Exception):
	pass
