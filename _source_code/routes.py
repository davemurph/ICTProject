# ICT Project 2014
# D Murphy
#
# routes.py

# imports
from _source_code import app
from flask import Flask, request, redirect, url_for, render_template, flash
from forms import ConversionForm, ResultForm, EnterForm
from rates import getRate, getSpecificRate, exchange

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
			unformatted_input_amount = float(form.conversionAmount.data)
			from_currency = form.fromCurrency.data
			to_currency = form.toCurrency.data			
			
			converted_amount = exchange(from_currency, to_currency, unformatted_input_amount)
			specific_rate = getSpecificRate(from_currency, to_currency)
			
			input_amount = '%.2f' % (unformatted_input_amount)
			
			return render_template('conversion.html', form=form, input_amount=input_amount, 
				from_currency=from_currency, to_currency=to_currency, 
				converted_amount=converted_amount, specific_rate=specific_rate)

	elif request.method == 'GET':		
		return render_template('conversion.html', form=form)
