from flask import Flask, render_template, request, Response
from bs4 import BeautifulSoup
import requests
import json

PLACES = [
        {'state' : 'Alabama', 'city' :'Phenix-City'},
        {'state' : 'Georgia', 'city' :'Columbus'}
]

def search_person(first, last, state, city):
    url = 'http://www.spokeo.com/' + first + '-' + last + '/' + state + '/' + city
    r = requests.get(url)
    return r

def get_data(data):
    data = json.loads(data)
    info = data['people']
    results = []
    for item in info:
        d = {'name'      : item['name'],      'dob'       : item['dob'],
             'age'       : item['age'],       'locations' : item['locations'],
             'longitude' : item['longitude'], 'includes'  : item['includes'],
             'relatives' : item['relatives'], 'latitude'  : item['latitude'],
             'aliases'   : item['aliases'] }
        results.append(d)
    return results

def query_person(first, last):
    for place in PLACES:
        r = search_person(first, last, place['state'], place['city'])
        soup = BeautifulSoup(r.text)
        results = []
        for script in soup.find_all('script'):
            if 'var search = {' in script.text:
                script_string = str(script)
                results += (get_data(script_string[script_string.index('{'): -10]))
        return results

application = Flask(__name__)

@application.route('/', methods=["POST", "GET"])
def search():
	if request.method == "GET":
		return render_template('search.html')
	if request.method == "POST":
		first = request.form["firstname"].split()[0].capitalize()
		last = request.form["lastname"].split()[0].capitalize()
		return render_template('searchresults.html', data=query_person(first, last))

if __name__ == "__main__":
    application.run(host='0.0.0.0', debug=True)