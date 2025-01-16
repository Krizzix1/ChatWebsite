from flask import Flask, render_template, url_for, redirect, jsonify, request, session, flash
from Messages.messages import messageBP

import database, security

app = Flask(__name__)
app.register_blueprint(messageBP, url_prefix="/messages")

#figure out this more later however its needed to stop users going straight to home page without logging in
app.secret_key = security.gen_secret_key()

public_key, private_key = security.gen_key_pair()

public_key_str = public_key.decode('utf-8')
private_key_str = private_key.decode('utf-8')

# Now replace any literal '\\n' with actual newlines (if they exist in the decoded string)
public_key_str = public_key_str.replace(r"\\n", "\n")
private_key_str = private_key_str.replace(r"\\n", "\n")
print(f"\nPubKey {public_key_str}\n")
print(f"\nPubKey {private_key_str}\n")


@app.route("/public-key", methods=["GET"])
def public_key_route():
    return jsonify({"public_key" : public_key.decode()})


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        action = request.form["action"]
        if action == "login":
            return redirect(url_for("login"))
        elif action == "signup":
            return redirect(url_for("signup"))
    return render_template("home.html")


@app.route("/logout", methods=["GET","POST"])
def logout():
    session.pop("username", None)
    flash("You have been logged out")
    return redirect(url_for("index"))

@app.route("/login", methods=["GET", "POST"])
def login():
    print(session)
    if "username" in session:
        return redirect(url_for("main"))
    if request.method == "POST":



        login_data = request.get_json()

        username = login_data.get("username")
        password = login_data.get("password")

        password = security.decrypt(password, private_key)
        

        '''
        The following is an example of good code
        the readability is improved by using a method
        known as "early return"
        '''
        if not database.existing_user(username):
            print(f"user {username} does not exist")
            flash("Incorrect username or password")
            return jsonify({"redirect_url": url_for("login")})
        if not database.validate_user_password(username, password):
            print("Incorrect password")
            flash("Incorrect username or password")
            return jsonify({"redirect_url": url_for("login")})
        session["username"] = username
        return jsonify({"redirect_url": url_for("main")})
    
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

        signup_data = request.get_json()

        username = signup_data.get("username")
        password = signup_data.get("password")

        password = security.decrypt(password, private_key)

        if database.existing_user(username):
            print(f"user {username} exists")
            return jsonify({"message": "User already exists"}), 400
        else:
            database.add_user(username, password)
            session["username"]=username
            return jsonify({"redirect_url": url_for("main")}), 200
    return render_template("signup.html")


@app.route("/main", methods=["GET","POST"])
def main():
    if "username" not in session:
        print("You must login first")
        flash("You must login first")
        return redirect(url_for("login"))
    return render_template("main.html", username=session["username"])


app.run(host="localhost",port=5001)
