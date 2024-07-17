from flask import Flask,render_template, request,redirect,url_for
import random

app = Flask(__name__)

@app.route("/home", methods={"GET","POST"})
def home():
    if request.method == "GET":
        return render_template("home.html")
    else:
        if (len(request.form["month"]) > 9):
            return redirect(url_for('fortune', month="september"))
        
        return redirect(url_for('fortune', month=request.form["month"]))

@app.route("/fortune/<month>")
def fortune(month):
    forunes = ["good day", "bad day", "ok day", "your dad will die", "it's your birthday", "you will get a gift", "you will die", "you will get hurt", "you will buy something", "it's your moms birthday"]
    return render_template("fortune.html", fortune=forunes[len(month)-1])


if __name__ == '__main__':
    app.run(debug=True)