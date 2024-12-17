from flask import Flask, render_template, request, url_for, redirect, session

import database, security

app = Flask(__name__)

#figure out this more later however its needed to stop users going straight to home page without logging in
app.secret_key = security.gen_secret_key()

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

        '''
        The following is an example of good code
        the readability is improved by using a method
        known as "early return"
        '''

        if not database.existing_user(username):
            print(f"user {username} does not exist")
            return render_template("login.html")
        if not database.validate_user_password(username, password):
            print("Incorrect password")
            return render_template("login.html")
        session["username"] = username
        return redirect(url_for("main"))
    
        '''
        The following is the same code as above but coded
        in a worse format regarding readability
        leaving these comments here as an example of how
        to improve code readability
        '''

        # if database.existing_user(username):
        #     if database.validate_user_password(username, password):
        #         session["username"] = username
        #         return redirect(url_for("main"))
        #     else:
        #         print("Incorrect password")
        # else:
        #     print(f"user {username} does not exist")
        
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
    if "username" not in session:
        print("You must login first")
        return redirect(url_for("login"))
    return render_template("main.html")



app.run(host="localhost",port=5001)