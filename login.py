from flask import render_template, request, redirect, flash, session
import dbconnection
import bcrypt
from flask_toastr import Toastr

toastr = Toastr()


def login_page():
    return render_template("login.html")


def authenticate_admin():
    if session.get("name"):
        return render_template('home.html')


    req = request.form

    missing = list()

    for k, v in req.items():
        if v == "":
            missing.append(k)

    if missing:
        feedback = f"Missing fields for {', '.join(missing)}"
        return render_template("login.html", feedback=feedback)

    email = request.form["email"]
    password = request.form["password"]

    query = {'email': email.lower()}
    collection_name = dbconnection.db["admins"]

    user = collection_name.find_one(query)

    if (bcrypt.checkpw(password.encode("utf-8"), user['password'])):
        session["name"] = request.form.get("name")
        flash(f"Logged In as {user['name']}", 'success')
        return render_template('home.html', user=user)

    flash("Invaild Credentials", 'error')
    return render_template("login.html")
