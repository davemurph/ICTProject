from flask import json
import requests
from requests.exceptions import ConnectionError


# set up dummy user for authentication, to match authenticated
# user in exchange_api
user = ('daithi', 'pass1234')


class Currencies():

	api_getcurrencies_url = 'http://localhost:8000/testapi/getcurrencies'
	headers = {'Content-Type': 'application/json'}		
		
	def test_feed_connection(self):
		try:
			currency_request = requests.get(self.api_getcurrencies_url, headers=self.headers, auth=user)
			if currency_request.status_code == 200:
				self.request_status_code = 200
				return True

			else:
				if currency_request.status_code == 403:
					self.request_status_code = 403
				elif currency_request.status_code == 404:
					self.request_status_code = 404
				return False

		except ConnectionError as error:
			self.request_status_code = 'connection_error'	
			return False

	def get_currency_list(self):
		json_currencies = requests.get(self.api_getcurrencies_url, headers=self.headers, auth=user)
		return json_currencies.json()
