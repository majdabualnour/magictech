import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import datetime
import requests
import random
import string
from firebase_admin import storage
from werkzeug.utils import secure_filename
cred = credentials.Certificate('magictech-a68b3-firebase-adminsdk-9exhf-c8ad41ef83.json')

appd = firebase_admin.initialize_app(cred,
                                     {
    'storageBucket': 'magictech-a68b3.appspot.com'
})

db = firestore.client()



# Sign in with email and password

api_key = 'AIzaSyBNhRKzdEIozqlyhV4BL5StGKhWvPQZPvc'

# Construct the sign-in endpoint URL
url = f"https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword?key={'AIzaSyBNhRKzdEIozqlyhV4BL5StGKhWvPQZPvc'}"
def creat_user(email , password):
    # Create a new user with email and password
    try:
        user = auth.create_user(
            email=email,
            password=password
        )
        return True
    except:
        return False
    

def upload_picture( file):
    bucket = storage.bucket()
    picture_blob = bucket.blob('profile_pictures/' + file.filename)
    picture_blob.upload_from_file(file)
    # image_url = picture_blob.public_url
    filename = secure_filename(file.filename)
    blob = bucket.blob(filename)


    file.seek(0)

    # Upload the file
    blob.upload_from_file(file)

    # Set public access
    blob.make_public()

    # Get the public URL
    url = blob.public_url
    # Get the public URL


    return url



def changedata(type , name , email ,occ,lan, pre):
    doc_ref = db.collection("users").document(f"{type}")
    doc_ref.set({"name": f"{name}", "email": f"{email}", "occupation": f'{occ}', "languages": f'{lan}', "premissions": f'{pre}'})

def adduser(type , name , email ,occ,lan, pre):
    # Choose the collection where you want to add the new document
    collection_ref = db.collection("users")
    date = datetime.datetime.now().date()
    # Create a Python dictionary representing the data for the new document
    data = {"name": f"{name}", "email": f"{email}", "occupation": f'{occ}', "languages": f'{lan}', "premissions": f'{pre}' , "date": f"{date}"}

    # Add the new document to the collection
    # new_doc_ref = collection_ref.add(data)
    # new_doc_id = new_doc_ref[1].id  # Retrieve the generated document ID

    # Alternatively, if you want to specify a custom document ID
    doc_ref = collection_ref.document(str(type))
    doc_ref.set(data)
def update(date , dead , pro):


    # Initialize Firestore client
    db = firestore.client()

    # Define the document path and field values to update
    
    collection_ref = db.collection("projects")
    field_updates = {

    'deadline': f'{dead}',
    'meeting_date': f'{date}'
    }

    # Update the document
    doc_ref = collection_ref.document(pro)
    doc_ref.update(field_updates)
def done(date , pro):
    db = firestore.client()
    collection_ref = db.collection("projects")
    field_updates = {

    'status': f'{date}'

    }

    # Update the document
    doc_ref = collection_ref.document(pro)
    doc_ref.update(field_updates)



def adduser(type , name , email ,occ,lan, pre,url):
    # Choose the collection where you want to add the new document
    collection_ref = db.collection("users")
    date = datetime.datetime.now().date()
    # Create a Python dictionary representing the data for the new document
    data = {"name": f"{name}", "email": f"{email}", "occupation": f'{occ}', "languages": f'{lan}', "premissions": f'{pre}' , "date": f"{date}","img": f"{url}"}

    # Add the new document to the collection
    # new_doc_ref = collection_ref.add(data)
    # new_doc_id = new_doc_ref[1].id  # Retrieve the generated document ID

    # Alternatively, if you want to specify a custom document ID
    doc_ref = collection_ref.document(str(type))
    doc_ref.set(data)

def logd_in(email , password):

    payload = {
        "email": email,
        "password": password,
        "returnSecureToken": True
    }


    response = requests.post(url, json=payload)
    data = response.json()

    if 'error' in data:

        error_message = data['error']['message']
        return error_message
    else:

        id_token = data['idToken']
        local_id = data['localId']
        return True
               
        # print('ID Token:', id_token)
        # print('Local ID:', local_id)
def seachnamebyemail(email):
    collection_ref = db.collection("users")        
    documents = collection_ref.get()

    for doc in documents:
        if doc.to_dict()['email'] == email:
            return doc.to_dict()['img'], doc.to_dict()['name']
def getallorderss(name):
    searched_users = []
    dectomatrix = []
    collection_ref = db.collection("projects")        
    documents = collection_ref.get()

    for doc in documents:
        if str(name).lower()  in str(doc.to_dict()['code']).lower()  :

            dectomatrix.append(doc.to_dict()['email'])
            dectomatrix.append(doc.to_dict()['date'])
            dectomatrix.append(doc.to_dict()['name'])
            dectomatrix.append(doc.to_dict()['project_name'])
            dectomatrix.append(doc.to_dict()['category'])
            dectomatrix.append(doc.to_dict()['status'])
            dectomatrix.append(doc.to_dict()['code'])
            dectomatrix.append(doc.to_dict()['phone'])
            dectomatrix.append(doc.to_dict()['idea'])
            dectomatrix.append(doc.to_dict()['deadline'])
            dectomatrix.append(doc.to_dict()['meeting_date'])
            searched_users.append(dectomatrix)
            dectomatrix = []
    return searched_users
def getallorders(name):
    searched_users = []
    dectomatrix = []
    collection_ref = db.collection("projects")        
    documents = collection_ref.get()
    if name == 'get_all':
        for doc in documents:
            dectomatrix.append(doc.to_dict()['email'])
            dectomatrix.append(doc.to_dict()['date'])
            dectomatrix.append(doc.to_dict()['name'])
            dectomatrix.append(doc.to_dict()['project_name'])
            dectomatrix.append(doc.to_dict()['category'])
            dectomatrix.append(doc.to_dict()['status'])
            dectomatrix.append(doc.to_dict()['code'])
            searched_users.append(dectomatrix)
            dectomatrix = []
        return searched_users
    elif name == 'get_done':
        d = 0 
        for doc in documents:
            d+=1
            if 'Done'.lower() in str(doc.to_dict()['status']).lower()  :
                dectomatrix.append(doc.to_dict()['code'])
                dectomatrix.append(doc.to_dict()['name'])
                dectomatrix.append(doc.to_dict()['project_name'])
                
                dectomatrix.append(doc.to_dict()['date'])
                dectomatrix.append(doc.to_dict()['status'])
                dectomatrix.append(doc.to_dict()['category'])
                dectomatrix.append(doc.to_dict()['email'])

                searched_users.append(dectomatrix)
                dectomatrix = []
        return searched_users, d
    elif name == 'waiting':
        countdo = 0 
        count = 0
        for doc in documents:
            if 'wait'.lower() in str(doc.to_dict()['status']).lower()  :
                count += 1
                
                dectomatrix.append(doc.to_dict()['code'])
                dectomatrix.append(doc.to_dict()['name'])
                dectomatrix.append(doc.to_dict()['project_name'])
                
                dectomatrix.append(doc.to_dict()['date'])
                dectomatrix.append(doc.to_dict()['status'])
                dectomatrix.append(doc.to_dict()['category'])
                dectomatrix.append(doc.to_dict()['email'])

                searched_users.append(dectomatrix)
            
                dectomatrix = []
            else:countdo +=1
      
        return searched_users , count ,countdo  
    elif name == 'waitingh':
        countdo = 0 
        count = 0
        for doc in documents:
            if 'wait'.lower() in str(doc.to_dict()['status']).lower()  :
                count += 1
                
                dectomatrix.append(doc.to_dict()['code'])
                dectomatrix.append(doc.to_dict()['name'])
                dectomatrix.append(doc.to_dict()['project_name'])
                
                dectomatrix.append(doc.to_dict()['date'])
                dectomatrix.append(doc.to_dict()['status'])
                dectomatrix.append(doc.to_dict()['category'])

              
                searched_users.append(dectomatrix)
            
                dectomatrix = []
            else:countdo +=1
      
        return searched_users , count ,countdo  

    else :
        for doc in documents:
            if str(name).lower()  in str(doc.to_dict()['project_name']).lower()  :
                dectomatrix.append(doc.to_dict()['code'])
                dectomatrix.append(doc.to_dict()['name'])
                dectomatrix.append(doc.to_dict()['project_name'])
                
                dectomatrix.append(doc.to_dict()['date'])
                dectomatrix.append(doc.to_dict()['status'])
                dectomatrix.append(doc.to_dict()['category'])
                dectomatrix.append(doc.to_dict()['email'])
                # dectomatrix.append(doc.to_dict()['email'])
                # dectomatrix.append(doc.to_dict()['date'])
                # dectomatrix.append(doc.to_dict()['name'])
                # dectomatrix.append(doc.to_dict()['project_name'])
                # dectomatrix.append(doc.to_dict()['category'])
                # dectomatrix.append(doc.to_dict()['status'])
                # dectomatrix.append(doc.to_dict()['code'])
                # dectomatrix.append(doc.to_dict()['phone'])
                # dectomatrix.append(doc.to_dict()['idea'])
                # dectomatrix.append(doc.to_dict()['deadline'])
                # dectomatrix.append(doc.to_dict()['meeting_date'])
                searched_users.append(dectomatrix)
                dectomatrix = []
        return searched_users

        
def getallusers(name):
    searched_users = []
    dectomatrix = []
    collection_ref = db.collection("users")        
    documents = collection_ref.get()
    count = 0
    if name == 'get_all':
        for doc in documents:
            dectomatrix.append(doc.to_dict()['name'])
            dectomatrix.append(doc.to_dict()['email'])
            dectomatrix.append(doc.to_dict()['occupation'])
            dectomatrix.append(doc.to_dict()['premissions'])
            dectomatrix.append(doc.to_dict()['languages'])
            dectomatrix.append(doc.to_dict()['date'])
            dectomatrix.append(doc.to_dict()['img'])
            searched_users.append(dectomatrix)
            dectomatrix = []
            count +=1
        return searched_users 
    else :
        for doc in documents:
            if str(name).lower() in str(doc.to_dict()['name']).lower()  :
                dectomatrix.append(doc.to_dict()['name'])
                dectomatrix.append(doc.to_dict()['email'])
                dectomatrix.append(doc.to_dict()['occupation'])
                dectomatrix.append(doc.to_dict()['premissions'])
                dectomatrix.append(doc.to_dict()['languages'])
                dectomatrix.append(doc.to_dict()['date'])
                dectomatrix.append(doc.to_dict()['img'])
                searched_users.append(dectomatrix)
                dectomatrix = []
        return searched_users

def addadmin( name , email ,occ,lan, pre , passw , url):
    # print(f'{creat_user(email , str(passw))}dddd')
    if  creat_user(email , str(passw))  :
        
        adduser(name , name , email ,occ,lan, pre   , url)
    else:
        return logd_in(email , passw)
# addadmin( 'Majd Abu Al-Nour' , 'majdapoalnoor@gmail.com' ,'Ai developer','python', 'Manager' , '1m2a3j4d')
def start(type , name , email ,phone, cat,idea , date ,dateline ):
    # Choose the collection where you want to add the new document
    collection_ref = db.collection("projects")
    code = generate_unique_id()
    datetoday = datetime.datetime.now().date()
    # date = datetime.datetime.now().date()
    # Create a Python dictionary representing the data for the new document
    data = {"name": f"{name}", "email": f"{email}", "phone": f'{phone}', "project_name": f'{type}', "category": f'{cat}' ,"idea": f"{idea}" ,  "meeting_date": f"{date}", "deadline": f"{dateline}" , 'code':code , 'date' :f'{datetoday}'  , 'status' : 'Waiting' }
    # Add the new document to the collection
    # new_doc_ref = collection_ref.add(data)
    # new_doc_id = new_doc_ref[1].id  # Retrieve the generated document ID

    # Alternatively, if you want to specify a custom document ID
    doc_ref = collection_ref.document(str(type))
    doc_ref.set(data)
    return code

def generate_unique_id(length=8):
    characters = string.ascii_letters + string.digits
    unique_id = ''.join(random.choice(characters) for _ in range(length))
    return unique_id
# start('fsf' , 'd' , 'd' , 'fasdf' , 'fsdf' , 'sfasf ' , 'sadfsa ' , 'sdfsafsa')
def deleteuser(name):
    collection_ref = db.collection("users")
    doc_ref = collection_ref.document(name)
    doc_ref.delete()

def getmeetdates():

    dectomatrix = []
    collection_ref = db.collection("projects")        
    documents = collection_ref.get()

    for doc in documents:
        dectomatrix.append((str(doc.to_dict()['meeting_date']).replace('/' , '-')).replace(' ' , 'T'))
    return dectomatrix