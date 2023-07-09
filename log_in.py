import requests

# Sign in with email and password

api_key = 'AIzaSyBNhRKzdEIozqlyhV4BL5StGKhWvPQZPvc'

# Construct the sign-in endpoint URL
url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={'AIzaSyBNhRKzdEIozqlyhV4BL5StGKhWvPQZPvc'}"
def logd_in(email , password):
    # email = 'mlljdaboalnoor@gmail.com'
    # password = '4444ss'

    # Create the sign-in request payload
    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }

    # Send the sign-in request
    response = requests.post(url, json=payload)
    data = response.json()

    if 'error' in data:
        # Handle authentication error
        error_message = data['error']['message']
        print('Sign in failed:', error_message)
    else:
        # Successful sign-in
        id_token = data['idToken']
        local_id = data['localId']
        return True
        # print('ID Token:', id_token)
        # print('Local ID:', local_id)
logd_in('affasdfasf'  , 'afaf')