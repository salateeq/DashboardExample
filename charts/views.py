from django.http import HttpResponse,JsonResponse
from django.shortcuts import redirect,render
import urllib.request
import json

def index(request,ctx={},template_file="dashboard/demo.html"):
    # return HttpResponse("Hello, world. You're at the polls index.")
    ctx["internet_users"] = 0
    ctx["internet_access"] = 0
    ctx["internet_access_in_schools"] = 0
    ctx["individuals_using_the_internet"] = 0
    ctx["internet_access_map"] = []
    
    return render(request,template_file,ctx)


def sources(request,ctx={},template_file="dashboard/sources.html"):
    # return HttpResponse("Hello, world. You're at the polls index.")
    # ctx[""]

    return render(request,template_file,ctx)



def internet_users(request,countryname,date2):
    Api_url = "https://tcdata360-backend.worldbank.org/api/v1/data?countries={0}&indicators=41384&timeframes={1}".format(countryname,date2)
    result = json.load(urllib.request.urlopen(Api_url))
    value = result['data']
    
    users_count = 0
    print(value)
    if(len(value)>0):
        users_count = value[0]['indicators'][0]['values'][str(date2)]
    else:
        users_count = 'NA'
    returnjson = {"users_count":users_count}
    print(returnjson)
    return JsonResponse(returnjson)


def internet_access(request,countryname,date2):
    Api_url = "https://tcdata360-backend.worldbank.org/api/v1/data?countries={0}&indicators=45346&timeframes={1}".format(countryname,date2)
    result = json.load(urllib.request.urlopen(Api_url))
    value = result['data']
    
    users_count = 0
    if(len(value)>0):
        users_count = value[0]['indicators'][0]['values'][str(date2)]
    else:
        users_count = 'NA'
    returnjson = {"access_count":users_count}
    print(returnjson)
    return JsonResponse(returnjson)



def internet_access_in_schools(request,countryname,date2):
    dateformat = "{0}-{1}".format(date2,int(date2)+1)
    date2 = dateformat
    Api_url = "https://tcdata360-backend.worldbank.org/api/v1/data?countries={0}&indicators=572&timeframes={1}".format(countryname,date2)
    result = json.load(urllib.request.urlopen(Api_url))
    value = result['data']
    
    users_count = 0
    if(len(value)>0):
        users_count = value[0]['indicators'][0]['values'][str(date2)]
    else:
        users_count = "NA"
    returnjson = {"internet_access_in_schools":users_count}
    print(returnjson)
    return JsonResponse(returnjson)


def individuals_using_the_internet(request,countryname,date2):
    Api_url = "https://tcdata360-backend.worldbank.org/api/v1/data?countries={0}&indicators=45410&timeframes={1}".format(countryname,date2)
    result = json.load(urllib.request.urlopen(Api_url))
    print(result,'result')
    value = result['data']
    users_count = 0
    if(len(value)>0):
        users_count = value[0]['indicators'][0]['values'][str(date2)]
    else:
        users_count = "NA"
    returnjson = {"individuals_using_the_internet":users_count}
    print(returnjson)
    return JsonResponse(returnjson)

def internet_access_map(request,date2):
    
    Api_url = "https://tcdata360-backend.worldbank.org/api/v1/data?indicators=41384&timeframes={0}".format(date2)
    result = json.load(urllib.request.urlopen(Api_url))
    resultedData = result['data']
    returnedData = []
    for countrydata in resultedData:
        id = convert_country_3letters_to_2letters(countrydata["id"])
        name = convert_country_3letters_to_countryName(countrydata["id"])
        value = countrydata["indicators"][0]["values"][date2]
        print(countrydata["id"])
        lat , long= convert_country_3letters_to_geolLocation(countrydata["id"])
        singeCountrydata = {"id":id,"name":name,"value":value,  "lat":lat,
  "long": long,
  "width": 1,
  "height": 1,
  "name_3_letters":countrydata["id"]}
        returnedData.append(singeCountrydata)
    return JsonResponse(returnedData,safe=False)



def convert_country_3letters_to_2letters(country3letters):

    data = json.load(open('charts/lookup/country_mapping.json', 'r'))
    countryName2letters = ''
    for i in data:
        if i['country3letters'] == country3letters:
            countryName2letters = i['country2letters']
            break
    return countryName2letters

def convert_country_3letters_to_countryName(country3letters):

    data = json.load(open('charts/lookup/country_mapping.json', 'r'))
    countryname = ''
    for i in data:
        if i['country3letters'] == country3letters:
            countryname = i['countryname']
            break
    return countryname


def convert_country_3letters_to_geolLocation(country3letters):
    data = json.load(open('charts/lookup/country_to_geolocation.json', 'r'))
    lat = ''
    long = ''
    for i in data:
        if i['alpha3'] == country3letters:
            lat = i['latitude']
            long = i['longitude']
            break
    return lat,long