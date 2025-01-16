from flask import Blueprint, render_template, session, redirect, request, url_for, flash, jsonify

import security, database



loginBP = Blueprint("loginBP",__name__,static_folder="static",template_folder="templates")

public_key, private_key = security.gen_key_pair()


@loginBP.route("/public-key", methods=["GET"])
def public_key_route():
    return jsonify({"public_key" : public_key.decode()})


@loginBP.route("/", methods=["GET", "POST"])
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
            return jsonify({"redirect_url": url_for("loginBP.login")})
        if not database.validate_user_password(username, password):
            print("Incorrect password")
            flash("Incorrect username or password")
            return jsonify({"redirect_url": url_for("loginBP.login")})
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




