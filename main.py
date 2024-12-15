from flask import Flask, render_template, request

import database

app = Flask(__name__)

@app.route("/", methods=["GET","POST"])
def index():
    if request.method == "POST":
        userInput = request.form["name"]
        print(userInput)
        database.add_entry(userInput)
        return render_template("home.html")
    return render_template("home.html")



app.run(host="localhost",port=5001)