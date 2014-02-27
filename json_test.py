import json
import urllib2


data = json.load(urllib2.urlopen('http://localhost:5000/testapi/getrates'))

print data

# convert params to JSON
	# json_params = json.dumps(request_params)
		
	# POST request to exchange_api with JSON params
	#post_request = urllib2.Request(api_convert_url, json_params, 
	#							{'Content-Type': 'application/json'})
	#openreq = urllib2.urlopen(post_request)
	#json_response = openreq.read()
	#openreq.close()
			
	# decode JSON response from request
	#result = json.loads(json_response)
	
	#currencies = json.load(urllib2.urlopen('http://localhost:8000/testapi/getcurrencies'))
