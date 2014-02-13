# ICT Project 2014
# D Murphy
#
# rates.py
# exchange rates and conversion functions
# getSpecificRate() and exchange() return Strings
# getRate() returns a float

# populateCurrencyList() returns a list of currencies from 
# dicts in exchange_rates to populate WTForms SelectFields


# exchange rates are relative to 1.0 * Euro
exchange_rates = 	{'EUR': 1.0, 
					'USD': 1.36379, 
					'GBP': 0.82910, 
					'AUD': 1.51202, 
					'CAD': 1.50140, 
					'NZD': 1.64072}

def populateCurrencyList():
	currencyList = []
	for currency in exchange_rates:
		currencyList.append((currency, currency))
		
	return currencyList

def getRate(currency):
	if currency in exchange_rates:
		return exchange_rates[currency]
		
def getSpecificRate(from_currency, to_currency):
	from_rate = exchange_rates[from_currency]		
	to_rate = exchange_rates[to_currency]
		
	return '%.5f' % (to_rate / from_rate)
			
def exchange(from_currency, to_currency, amount):
	from_rate = exchange_rates[from_currency]		
	to_rate = exchange_rates[to_currency]
		
	return '%.2f' % (amount * to_rate / from_rate)
	
