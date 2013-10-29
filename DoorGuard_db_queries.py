import requests
import json

#store the api key in a separate file so I don't accidentally upload it to github
api_key = open("api_key.secret").read()
base_url = "https://admin.doorguardhq.com"
headers = {'content-type': 'application/json', 'Accept':'application/json'}

def deal_with_errors(r):
	if not (r.status_code == requests.codes.ok): print r.json()
	r.raise_for_status() #rases an exception based on the response code

def list_people(since = None):
	#"{0}-{1}-{2}T{3}:{4}:{5}".format(*time.localtime())
	r = requests.get(
		base_url + "/api/1/people.json",
		params = {"api_key": api_key, "since":since},
		headers = headers
		)
	deal_with_errors(r)
	return r.json() #requests has a built in json parser.

def create_person(person):
	"takes a dict representing the user to be added"
	r = requests.post(
		base_url + '/api/1/people',
		params = {"api_key": api_key},
		headers = headers,
		data = json.dumps(me)
		)
	deal_with_errors(r)
	return r

def update_person(id, person):
	"takes the id of the user and a dict representing the information to be changed"
	r = requests.put(
		'{url}/api/1/people/{id}'.format(url = base_url, id = id),
		params = {"api_key": api_key},
		headers = headers,
		data = json.dumps(person)
		)
	deal_with_errors(r)
	return r

def delete_person(id):
	'deletes the user with the given id'
	r = requests.delete(
		'{url}/api/1/people/{id}'.format(url = base_url, id = id),
		params = {"api_key": api_key},
		headers = headers,
		)
	deal_with_errors(r)
	return r

me = {
    "first_name": "Tom",
    "last_name": "Hodson",
    "pin": "1234",
    "key_fob_number": "1234",
    "enabled": True,
    "mobile": "",
    "notes": "",
    "telephone": "",    
    "email": "",
    "valid_from": "2011-11-01",
    "valid_to": "2014-11-25",
    "role_ids": []
}

def get_card_cache():
	return {p['key_fob_number'] : p['pin'] for p in list_people() if p['enabled'] == True}

if __name__ == '__main__':
	print get_card_cache()
