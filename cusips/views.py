from django.shortcuts import get_list_or_404, render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.utils import timezone
from django.db import IntegrityError

from cusips.models import Cusips

import requests

from local_settings import *

def index(request):
	return render(request, 'index.html')

def cusip_search(request):
	return render(request, 'cusip_entry_form.html')

#VIEW DESC: Return all bonds currently stored in the DB
#ARGS: [muni] - int as bool, should output be restricted to Municipal bonds only?
def get_bonds(request, muni, json):
	if muni == 1:
		res = get_list_or_404(Cusips.objects.filter(market_sector='Muni'))
	else:
		res = get_list_or_404(Cusips)
	print(list(res))
	if json == 1:
		return JsonResponse( serializers.serialize('json', res) , safe=False)
	else:
		return render(request, 'list.html', {'bonds':res})

#VIEW DESC: Ingest cusip's via GET request, use FIGI API to collect information on each bond and store all information
#ARGS: [cusip_csv] - Comma seperated value list of CUSIP's
def add(request):
	csv = request.POST.get("csv", "")

	cusips = csv.split(',')

	bonds = []
	for cusip in cusips:
		figijson = get_cusip_data(cusip)

		if 'error' in figijson:
			bonds.append( cusip + ": Invalid or network issues" )
			print("Something went wrong: " + figijson['error'])
			#'No identifier found.'
		else:
			bonds.append( cusip + ": (" + figijson['name'] + ") " + figijson['marketSector'])
			try:
				c = Cusips(cusip_code=cusip, ticker=figijson['ticker'], entity_name=figijson['name'], market_sector=figijson['marketSector'], security_type=figijson['securityType'], exchange_code=figijson['exchCode'], timestamp=timezone.now())
				c.save()
			except IntegrityError as e:
				#TODO: If these values can change over time, then it's probably a good idea to check for unique field check on cusip code and do an update instead of create if a bond is being re-checked (with updated timestamp)
				print(e)
			print(bonds)

	return render(request, 'list.html', {'bonds':bonds})

#EXTERNAL API: get FIGI data from OpenFIGI (API DOCS https://www.openfigi.com/api#post-v2-mapping)
#ARGS: CUSIP id
def get_cusip_data(cid):
	API_ENDPOINT = "https://api.openfigi.com/v2/mapping"
	#API_ENDPOINT = "https://postman-echo.com/post"
	data = [{'idType':'ID_CUSIP',
			'idValue': cid},]
	headers = {'Content-Type': 'application/json',
			'X-OPENFIGI-APIKEY': local_settings['figikey']
	}
	r = requests.post(url = API_ENDPOINT, json=data, headers=headers) 

	if 'data' in r.json()[0]:
		return r.json()[0]['data'][0]
	elif 'error' in r.json()[0]:
		return r.json()[0]
	else:
		return {'error': 'unknown error'}