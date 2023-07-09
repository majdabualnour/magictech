from flask import Flask, redirect, url_for, request,render_template , session
from firebase_admin import firestore
from flask_jwt_extended import jwt_required
import datafire
app = Flask(__name__)

app.secret_key = 'thetopsecretmajd1234'
db = firestore.client()
@app.route('/')
def home():
   user_agent = request.headers.get('User-Agent')

    # Detect the device type based on the user agent
   if 'Mobile' in user_agent or 'Android' in user_agent:
      device_type = 'Mobile'
   elif 'Tablet' in user_agent:
      device_type = 'Tablet'
   else:
      device_type = 'Desktop'

   # Update visit count in Firestore
   visit_ref = db.collection('visits').document(device_type)
   visit_doc = visit_ref.get()
   if visit_doc.exists:
      count = visit_doc.get('count') + 1
      visit_ref.update({'count': count})
   else:
      visit_ref.set({'count': 1})

   # Retrieve visit counts from Firestore
   visits = db.collection('visits').get()
   visit_counts = {doc.id: doc.get('count') for doc in visits}
   session['visits'] = visit_counts

   return render_template("home.html")


@app.route('/about')
def about():
   return render_template("about.html")


@app.route('/orders',methods = ['POST', 'GET'])
def orderss():
   if request.method == 'POST':
      search = request.form['search']
      data= datafire.getallorders(search)
      img = session.get('avatar')

      return render_template("orders.html" ,  data = data)
   img = session.get('avatar')
   data ,d,s= datafire.getallorders('waiting')


   return render_template("orders.html" , image_url = img , data = data )
   return render_template("about.html")
@app.route('/doneprojects',methods = ['POST', 'GET'])
def done():
   if request.method == 'POST':
      search = request.form['search']
      data= datafire.getallorders(search)
      img = session.get('avatar')

      return render_template("donepro.html" ,  data = data)
   img = session.get('avatar')
   data, d= datafire.getallorders('get_done')


   return render_template("donepro.html" , image_url = img , data = data )
@app.route('/services')
def services():
   return render_template("services.html")


@app.route('/our_projects')
def ourpro():
   return render_template("our_projects.html")
@app.route('/admins/<use>')
def admins(use):
   if 'username' in session:
      img = session.get('avatar')
      data = session.get('dataorders')
      majd = session.get('majd')
      countd = session.get('count')
      collection_ref = db.collection('users')
      
      # Get the documents in the collection
      documents = collection_ref.get()

      # Calculate the number of documents
      count = len(documents)
      
      visits = db.collection('visits').get()
      visit_counts = {doc.id: doc.get('count') for doc in visits}

      return render_template("admin.html" , name = use, image_url = img , data = data ,visit_counts = visit_counts , waited = majd , count= countd  , counta =count)
   else:
        return redirect(url_for('login'))
# @app.route('/addadmin')
# def addadmins():
   # if 'username' in session:
   #      return render_template("addadmin.html" )
   # else:
   #      return redirect(url_for('login'))
# @app.route('/log')
# def log():
#    return render_template("login.html")

# @app.route('/addadmin')
# def addadmin():
#    return render_template("addadmin.html")
@app.route('/code/<use>')
def code(use):
   
   data = datafire.getallorderss(use)
   print(data)
   if data != []:
      return render_template("getcode.html" , data = data )
   return render_template("home.html")
@app.route('/codea/<use>')
def codea(use):
   
   data = datafire.getallorderss(use)
   session['proname'] =data
   
   
   return render_template("ffas.html" , data = data )

   
@app.route('/false')
def false():
   return f'failed to find your acount '

@app.route('/addadmin',methods = ['POST', 'GET'])
def addadmin():
   if 'username' in session:
      
      if request.method == 'POST':
         file = request.files['picture']
         passw = request.form['pass']
         name = request.form['name']
         email = request.form['email']
         occ = request.form['occ']
         user = request.form['lan']
         per = request.form['per']
         url = datafire.upload_picture(file)
         dadtafire =datafire.addadmin( name , email ,occ,user, per , passw, url)

         if dadtafire != None:
            return dadtafire
         
      return render_template("addadmin.html" )
   else:
      return redirect(url_for('login'))   
      
      # # print(f'dd{user}')
      # if  user == False:
      #    return redirect(url_for('false' ))
      # else:
      #    session['username'] = user
      #    return redirect(url_for('admins', use = user ))
   # else:
   #    user = request.args.get('email')
   #    passw = request.args.get('pass')
   #    user = data.seacha(user,passw)
   #    # print(user')  
   #    if  user == False:
   #       return redirect(url_for('false' ))
   #    else:
   #       return redirect(url_for('admins', use = user ))
   return render_template("addadmin.html")
@app.route('/codeg',methods = ['POST', 'GET'])
def codeg():
   if request.method == 'POST':
      

      name = request.form['code']
      return  redirect(url_for('code', use = name ))
   else:
      return render_template('home.html')
@app.route('/save',methods = ['POST', 'GET'])
def codes():
   if request.method == 'POST':
      countd = session.get('proname')

      name = request.form['meet']
      dead = request.form['dead']
      datafire.update(name, dead,countd[0][3])
      return  redirect(url_for('codea', use = countd[0][6] ))
@app.route('/done',methods = ['POST', 'GET'])
def donde():
   if request.method == 'POST':
      countd = session.get('proname')
      print(countd)
      datafire.done('Done', countd[0][3])
      return  redirect(url_for('codea', use = countd[0][6] ))
   
@app.route('/contact',methods = ['POST', 'GET'])
def start():
   if request.method == 'POST':
      

      name = request.form['name']
      email = request.form['email']
      phone = request.form['phone']
      cat = request.form['cat']
      pname = request.form['pname']
      idea = request.form['idea']
      datetime = request.form['datetime']
      date = request.form['date']


    # Retrieve visit counts from Firestore

      code = datafire.start(pname,  name , email ,phone,cat, idea , datetime ,date)
      return render_template('code.html' , code = code)
   else:
      m  = datafire.getmeetdates()
      print(m)
      return render_template("contact.html" , dates =m )

@app.route('/login',methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user = request.form['email']
      passw = request.form['pass']
      userafter = datafire.logd_in(user, passw) 
      # print(f'dd{user}')
      if  userafter != True:
         return userafter
      else:
         imgd , user = datafire.seachnamebyemail(user)
         data,count ,countdo= datafire.getallorders('waitingh')
         counta = datafire.getallusers('get_all')
         session['username'] = user
         session['avatar'] = imgd
         session['dataorders'] =data
         session['majd'] = count
         session['count'] = countdo
         session['counta'] = counta
         return redirect(url_for('admins', use = user ))
   # else:
   #    user = request.args.get('email')
   #    passw = request.args.get('pass')
   #    user = data.seacha(user,passw)
   #    # print(user')  
   #    if  user == False:
   #       return redirect(url_for('false' ))
   #    else:
   #       return redirect(url_for('admins', use = user ))
   return render_template("login.html")

@app.route('/searchusers', methods=['GET', 'POST'])
def searchusers():
   if request.method == 'POST':
      search = request.form['search']
      data = datafire.getallusers(search)
      return render_template("searchusers.html" ,  data = data)
   data =  datafire.getallusers('get_all')
   return render_template("searchusers.html" ,  data = data)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


# @app.route('/deleteuser', methods=['GET', 'POST'])
# def deleteuser():
#    if request.method == 'POST':
#          search = request.form['search']
#          data = datafire.deleteuser(search)


if __name__ == '__main__':
   app.run(debug = True)