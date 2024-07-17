from flask import Flask,render_template
import random

app = Flask(__name__)

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/fortune")
def fortune():
    forunes = ["good day", "bad day", "ok day", "your dad will die", "it's your birthday", "you will get a gift", "you will die", "you will get hurt", "you will buy something", "it's your moms birthday"]
    return render_template("fortune.html", fortune=forunes[random.randint(0,9)])

if __name__ == '__main__':
    app.run(debug=True)