from flask import Flask, render_template, request, redirect, url_for
from flask import session as login_session 
import pyrebase

app = Flask(__name__)
app.config['SECRET_KEY']="*******"

firebaseConfig = {
  'apiKey': "AIzaSyANcpET6TVMGoXBTQ2p2c6hNrvydWk7SkM",
  'authDomain': "presonal-579b7.firebaseapp.com",
  'projectId': "presonal-579b7",
  'storageBucket': "presonal-579b7.appspot.com",
  'messagingSenderId': "350913839647",
  'appId': "1:350913839647:web:97c006d7af4ca894788b2a",
  "measurementId": "G-T49G274SEY",
  "databaseURL": "https://presonal-579b7-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

def addQuestion(title, text):
    user_id = login_session["user"]["localId"]
    user = db.child("users").child(user_id).get().val()
    
    new_question = {
        "user": user["username"],
        "title": title,
        "text": text
    }
    db.child("questions").push(new_question)
    
    if "questions" not in user or user["questions"] is None:
        previous_questions = []
    else:
        previous_questions = user["questions"]
        
    previous_questions.append(new_question)
    db.child("users").child(user_id).update({"questions": previous_questions})


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if request.args.get("f") == "signin":
            return redirect(url_for("signin"))
        elif request.args.get("f") == "signup":
            return redirect(url_for("signup"))
        elif request.args.get("f") == "signout":
            login_session["user"] = None
            return redirect(url_for("signin"))
        elif request.args.get("f") == "addQuestion":
            if "user" in login_session and  login_session["user"] is not None:
                addQuestion(request.form["title"], request.form["text"])
            
    if "user" in login_session and not login_session["user"] == None:
        username_var =db.child("users").child(login_session["user"]["localId"]).get().val()["username"]
    else:
        username_var = "t"
        
    return render_template("home.html", 
                           signedin="user" in login_session and login_session["user"] is not None,
                           username=username_var,
                           questions_available =  db.child("questions").get().val() is not None,
                           questions= db.child("questions").get().val()
                           )

    
@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == "GET":
        return render_template("signin.html")
    
    try:
        login_session["user"] = auth.sign_in_with_email_and_password(request.form["email"], request.form["password"])
        return redirect(url_for('home'))
    except:
        return render_template("signin.html", error="something went wrong pls try again!")
    
    
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == "GET":
        return render_template("signup.html")
    
    try:
        login_session["user"] = auth.create_user_with_email_and_password(request.form["email"], request.form["password"])
        db.child("users").child(login_session["user"]["localId"]).set({
            "email": request.form["email"],
            "password": request.form["password"],
            "username": request.form["username"],
            "questions": []
        })
        return redirect(url_for('home'))
    except:
        return render_template("signup.html", error="something went wrong pls try again!")
    

    
if __name__ == "__main__":
    app.run(debug=True)