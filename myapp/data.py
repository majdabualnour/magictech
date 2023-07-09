import firebase_admin
from firebase_admin import credentials , db
import json
from passlib.hash import bcrypt_sha256

# Hash a password

cred_obj = firebase_admin.credentials.Certificate("magic-412fc-firebase-adminsdk-gt8hd-2dad5686c1.json")
default_app = firebase_admin.initialize_app(cred_obj, {
	'databaseURL':'https://magic-412fc-default-rtdb.firebaseio.com/'
	})


ref = db.reference("/")
# As an admin, the app has access to read and write all data, regradless of Security Rules
def custom_hash(message):
    prime = 31  # A prime number to use as the base
    modulus = 2**32  # Modulus to limit the hash value
    hash_value = 0

    for char in message:
        hash_value = (hash_value * prime + ord(char)) % modulus

    return hash_value

def check_hash(message, hash_value):
    prime = 31
    modulus = 2**32
    calculated_hash = custom_hash(message)

    return calculated_hash == hash_value
def checkpass(passw , passw2):
	if passw == passw2:
		return True
def seacha(gmail, passw):
	ref = db.reference("/")
	best_sellers = ref.get()
	for key, value in best_sellers.items():
		if(value["email"] == f"{gmail}"):
			if checkpass(passw , value['password']):
				d =  value['name']
				print(d)
				return d
			else:return False
		else: return False

	
def custom_hash(message):
    prime = 31  # A prime number to use as the base
    modulus = 2**32  # Modulus to limit the hash value
    hash_value = 0

    for char in message:
        hash_value = (hash_value * prime + ord(char)) % modulus

    return hash_value

def check_hash(message, hash_value):
    prime = 31
    modulus = 2**32
    calculated_hash = custom_hash(message)

    return calculated_hash == hash_value
