import requests

def generate_user():
    resp = requests.get("https://randomuser.me/api/")
    data = resp.json()
    stuff = data["results"][0]
    gender = stuff['gender']
    name = (stuff['name']['first'], stuff['name']['last'])
    city = stuff['location']['city']
    country = stuff['location']['country']
    email = stuff['email']
    username = stuff['login']['username']
    age = stuff['dob']['age']
    pic = stuff['picture']['large']

    return {
        'firstname' : name[0],
        'lastname' : name[1],
        'gender' : gender,
        'country' : country,
        'city' : city,
        'username' : username,
        'email' : email,
        'age' : age,
        'pic' : pic
    }