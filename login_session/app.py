from flask import Flask,render_template, request,redirect,url_for
from flask import session as login_session


app = Flask(__name__)
app.config["SECRET_KEY"] = "PASSWORD"

@app.route('/',methods=["GET","POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    
    login_session["name"] = request.form["name"]
    login_session["month"] = request.form["month"]
    return redirect(url_for('home'))
    
    
    
@app.route("/home", methods={"GET","POST"})
def home():
    if (not "month" in login_session.keys()) or (not "name" in login_session.keys()):
        login_session.clear()
        return redirect(url_for('login'))
    else:
        if request.method == "GET":
            return render_template("home.html", name=login_session["name"],month=login_session["month"])

        login_session.clear()
        return redirect(url_for('login'))

@app.route("/fortune")
def fortune():
    if (not "month" in login_session.keys()) or (not "name" in login_session.keys()):
        return redirect(url_for('login'))
    forunes = ["good day", "bad day", "ok day", "your dad will die", "it's your birthday", "you will get a gift", "you will die", "you will get hurt", "you will buy something", "it's your moms birthday"]
    return render_template("fortune.html", fortune=forunes[len(login_session["month"])-1])


if __name__ == '__main__':
    app.run(debug=True)