from flask import render_template, request, redirect, flash, session
import dbconnection
import bcrypt
from flask_toastr import Toastr
from logconfig import LogConfig

log_config = LogConfig()
logger = log_config.logger_config()

toastr = Toastr()

# Gets the Admin Login page
def login_page():
    logger.info('login_page() begins')
    if session.get("email"):
        return redirect('/')
    return render_template("login.html", title="Crestview - Admin Login")

# It validates the username and password entered by the user
def authenticate_admin():
    logger.info('authenticate_admin() begins')
    if session.get("email"):
        return redirect('/')


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

    if(not user):
        flash("User not found.", 'error')
        return redirect('/login')

    if (bcrypt.checkpw(password.encode("utf-8"), user['password'])):
        session["email"] = email
        flash(f"Logged In as {user['name']}", 'success')
        return redirect('/')

    flash("Invalid Credentials", 'error')
    return redirect('/login')


# It empties the session and logout the user.
def logout():
    logger.info('logout() begins')
    session.pop('email',None)
    flash("Logged out successfully.", 'success')
    return redirect('/login')