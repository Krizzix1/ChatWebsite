from flask import Flask, render_template, request, url_for, redirect

import database

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form["action"]
        if action == "login":
            return redirect(url_for("login"))
        elif action == "signup":
            return redirect(url_for("signup"))
    return render_template("home.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if database.existing_user(username):
            if database.validate_user_password(username, password):
                return redirect(url_for("main"))
            else:
                print("Incorrect password")
        else:
            print(f"user {username} does not exist")
    return render_template("login.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if database.existing_user(username):
            print(f"user {username} exists")
        else:
            database.add_user(username, password)
            return redirect(url_for("login"))
    return render_template("signup.html")


@app.route("/main")
def main():
    return render_template("main.html")



app.run(host="localhost",port=5001)