from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session 
import pyrebase

app = Flask(__name__)
app.config['SECRET_KEY']="*******"

   
firebaseConfig = {
  "apiKey": "AIzaSyCmVPwGebqkmcMzqRGwWRD_WIRPgEpnmN4",
  "authDomain": "auth-1d122.firebaseapp.com",
  "projectId": "auth-1d122",
  "storageBucket": "auth-1d122.appspot.com",
  "messagingSenderId": "904400603214",
  "appId": "1:904400603214:web:1a6134f512ebf7c3f51b1f",
  "measurementId": "G-07RG4NS2HQ",
  "databaseURL" : "https://auth-1d122-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'GET':
        return render_template("signin.html") 
    
    email = request.form['email']
    password = request.form['password']
    try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return redirect(url_for('home'))
    except:
        error_msg = "Womp it failed sad"
        return render_template("signin.html", error=error_msg)


@app.route('/', methods=["GET", "POST"])
def signup():
    if request.method == 'GET':
        return render_template("signup.html") 
    
    try:
        login_session['user'] = auth.create_user_with_email_and_password(request.form['email'], request.form['password'])
        db.child("users").child(login_session['user']['localId']).set(
            {"email": request.form['email'], 
            "password": request.form['password'],
            "username": request.form['username'],
            "full_name": request.form['full_name']
            })
        return redirect(url_for('home'))
    except:
        error_msg = "Womp it failed. Try again"
        return render_template("signup.html",error=error_msg)
        
    
@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("home.html")
    
    if request.args.get("f") == "f1":
        login_session["user"] = None
        auth.current_user = None
        return redirect(url_for('signin'))
    
    db.child("quotes").push({"quote":request.form["quote"],
                             "said_by":request.form["said_by"],
                             "id":login_session["user"]["localId"]})
    return redirect(url_for("thanks"))
    
    
    


@app.route('/thanks')
def thanks():
    return render_template("thanks.html")

@app.route('/display')
def display():
    return render_template("display.html", quotes=db.child("quotes").get().val())

if __name__ == '__main__':
    app.run(debug=True)
