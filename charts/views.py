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
    
    Api_url = "https://tcdata360-backend.worldbank.org/api/v1/data?indicators=1742&timeframes={0}".format(date2)
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

def convert_countryname_to_3letters(countryname):

    data = json.load(open('charts/lookup/country_mapping.json', 'r'))
    country3letters = ''
    for i in data:
        if i['countryname'] == countryname:
            country3letters = i['country3letters']
            break
    return country3letters




def High_Technology_Exports(request,countryname,date2):
    Api_url = "https://api.worldbank.org/v2/country/{0}/indicator/TX.VAL.TECH.MF.ZS?format=json&date={1}".format(countryname,date2)
    
    result = json.load(urllib.request.urlopen(Api_url))
    print(result,'result')
    # value = result[1][0]['value']
    users_count = 0
    if(len(result) >1):
        users_count = result[1][0]['value']
    else:
        users_count = 0
    returnjson = {"High_Technology_Exports":users_count}
    print(returnjson)
    return JsonResponse(returnjson)

def High_Technology_Exports_in_dollar(request,countryname,date2):
    Api_url = "https://api.worldbank.org/v2/country/{0}/indicator/TX.VAL.TECH.CD?format=json&date={1}".format(countryname,date2)
    
    result = json.load(urllib.request.urlopen(Api_url))
    print(result,'result')
    # value = result[1][0]['value']
    users_count = 0
    if(len(result) >1):
        users_count = result[1][0]['value']
    else:
        users_count = 0
    returnjson = {"High_Technology_Exports_in_dollar":users_count}
    print(returnjson)
    return JsonResponse(returnjson)



def individual_using_internet_vs_neighbouring_countries(request,countryname,date2):
    data = json.load(open('charts/lookup/Neighbouring_Countries.json', 'r'))
    NeighbouringCountries = []
    countryFullName = convert_country_3letters_to_countryName(countryname)
    NeighbouringCountriesString = countryname
    for i in data:
        if i['country1Label'] == countryFullName:
            NeighbouringCountry3LettersConverted = convert_countryname_to_3letters(i['country2Label'])
            if(len(NeighbouringCountry3LettersConverted)>0):
                NeighbouringCountries.append(NeighbouringCountry3LettersConverted)
                NeighbouringCountriesString = NeighbouringCountriesString+";"+NeighbouringCountry3LettersConverted
            
    Api_url = "https://api.worldbank.org/v2/country/{0}/indicator/IT.NET.USER.ZS?format=json&date={1}".format(NeighbouringCountriesString,date2)
    
    result = json.load(urllib.request.urlopen(Api_url))
    # print(result,'result')
    # value = result[1][0]['value']
    users_count = 0
    Data = []
    if(len(result) >1):
        users_count = result[1]
        MaximumCountriesCount = 0
        for i in users_count:
            if(i["value"]!=None):
                # {'indicator': {'id': 'IT.NET.USER.ZS', 'value': 'Individuals using the Internet (% of population)'}, 'country': {'id': 'AE', 'value': 'United Arab Emirates'}, 'countryiso3code': 'ARE', 'date': '2019', 'value': 99.14999998, 'unit': '', 'obs_status': '', 'decimal': 0}
                name = i["country"]['value']
                name2letters = i["country"]['id']
                value = i['value']
                print(name," ",value)
                image = "https://www.worldatlas.com/r/w960-q80/img/flag/{0}-flag.jpg".format(name2letters.lower())
                tempData = {"name":name,"steps":value,"href":image}
                if(i["countryiso3code"] == countryname):
                    Data.insert(0,tempData)
                else:
                    Data.append(tempData)
                MaximumCountriesCount = MaximumCountriesCount + 1
    else:
        users_count = 0

    returnjson = {"individual_using_internet_vs_neighbouring_countries":Data[0:6]}
    return JsonResponse(returnjson)
