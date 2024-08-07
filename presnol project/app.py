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

def add_question(title, text):
    user_id = login_session["user"]["localId"]
    user = db.child("users").child(user_id).get().val()
    
    new_question = {
        "user": user["username"],
        "title": title,
        "text": text,
        "comments": []
    }
    
    id = db.child("questions").push(new_question)["name"]
    if "questions_id" not in user or user["questions_id"] is None:
        previous_questions_id = []
    else:
        previous_questions_id = user["questions_id"]
        
    previous_questions_id.append({"id": id, "title": title})
    db.child("users").child(user_id).update({"questions_id": previous_questions_id})
    
     
    
    
    
def add_comment(questionId, text):
    question = db.child("questions").child(questionId).get().val()
    if "comments" not in question or question["comments"] is None:
        previous_questions = []
    else:
        previous_questions = question["comments"]
    
    previous_questions.append({
        "user": db.child("users").child(login_session["user"]["localId"]).get().val()["username"],
        "text": text
    })
    
    db.child("questions").child(questionId).update({"comments": previous_questions})

def check_exsisting_values():
    if "user" in login_session and not login_session["user"] == None:
        user = db.child("users").child(login_session["user"]["localId"]).get().val()
        username_var = user["username"]
        if "questions_id" in user and user["questions_id"] is not None:
            users_questions_var= user["questions_id"]
        else:
           users_questions_var = [] 
    else:
        username_var = "t"
        users_questions_var = []
    
    return [username_var, users_questions_var]

def create_user():
    login_session["user"] = auth.create_user_with_email_and_password(request.form["email"], request.form["password"])
    db.child("users").child(login_session["user"]["localId"]).set({
        "email": request.form["email"],
        "password": request.form["password"],
        "username": request.form["username"],
        "questions_id": []
    })
    


@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if request.args.get("f") == "signin":
            return redirect(url_for("signin"))
        
        elif request.args.get("f") == "signup":
            return redirect(url_for("signup"))
        
        elif request.args.get("f") == "signout":
            login_session["user"] = None
            auth.current_user = None
            return redirect(url_for("signin"))
        
        elif request.args.get("f") == "addQuestion" and "user" in login_session and  login_session["user"] is not None:
            add_question(request.form["title"], request.form["text"])
            
    values = check_exsisting_values()
        
    return render_template("home.html", 
                           signedin="user" in login_session and login_session["user"] is not None,
                           username=values[0],
                           questions_available =  db.child("questions").get().val() is not None,
                           questions= db.child("questions").get().val(),
                           users_questions = values[1]
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
        create_user()
        return redirect(url_for('home'))
    except:
        return render_template("signup.html", error="something went wrong pls try again!")
    
@app.route("/question/<string:questionId>", methods=['GET', 'POST'])
def question(questionId):
    if request.method == "POST" and "user" in login_session and  login_session["user"] is not None:
        add_comment(questionId, request.form["text"])
        
    question_data = db.child("questions").child(questionId).get().val()
    
    if "comments" not in question_data or question_data["comments"] is None:
        comments_list = []
    else:
        comments_list = question_data["comments"]
        
    values = check_exsisting_values()
        
    return render_template("question.html",
                           question=db.child("questions").child(questionId).get().val(),
                           comments=comments_list,
                           route="/question/"+questionId,
                           signedin="user" in login_session and login_session["user"] is not None,
                           username=values[0])
    
if __name__ == "__main__":
    app.run(debug=True)