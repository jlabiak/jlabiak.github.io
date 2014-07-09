from django.shortcuts import render
from django.core.cache import cache
import urllib
import json

def charts(request):

    cache_time = 600

    categories = cache.get('categories')
    if not categories:
        categories = getCategories()
        cache.set('categories', categories, cache_time)

    funding = cache.get('funding')
    if not funding:
        funding = getFunding()
        cache.set('funding', funding, cache_time)

    return render(request, 'charts.html', locals())

def getCategories():
    url = 'http://api.crunchbase.com/v/1/companies.js?api_key=hzy5vdwpnxzf9v2qjj28cvvs'
    companies = urllib.urlopen(url).read()
    jcompanies = json.loads(companies)

    categories = {}
    for company in jcompanies:
        if company['category_code'] in categories:
            categories[company['category_code']]+=1
        else:
            categories[company['category_code']]=1
    
    del categories[None]
    return categories

def getFunding():
    url = 'http://api.crunchbase.com/v/1/company/rockerbox.js?api_key=hzy5vdwpnxzf9v2qjj28cvvs'
    rockData = urllib.urlopen(url).read()
    jrockData = json.loads(rockData)

    funding = {}
    for rounds in jrockData['funding_rounds']:
        if rounds['funded_year'] in funding:
            funding[rounds['funded_year']] += rounds['raised_amount']
        else:
            funding[rounds['funded_year']] = rounds['raised_amount']

    return funding
