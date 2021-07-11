from flask import Flask, request, render_template, session, redirect
import dbconnection


import login
from user import User
from flask_toastr import Toastr
from flask_session import Session

app = Flask(__name__)
toastr = Toastr(app)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app.add_url_rule('/login', view_func=login.login_page)
app.add_url_rule('/authenticate', view_func=login.authenticate_admin, methods=['POST'])
app.add_url_rule('/logout', view_func=login.logout)


@app.route("/")
def test():
    if not session.get("email"):
        return redirect('/login')

    collection_name = dbconnection.db["admins"]
    user = collection_name.find_one()
    # return jsonify(message=single_record)
    # mydict = {"name": "John Doe", "email": "johndoe@gmail.com", "password" : "john123"}

    # x = collection_name.insert_one(mydict)
    # print(x)
    return render_template("home.html", user=user, title='Home')

@app.route("/add_new_user")
def add_new_user():
    user = User("Abhinav Mittal", "abhinavmittal93@gmail.com", "@Bhinav123")
    response = user.create_new_user(user)
    if(response):
        return 'User created successfully'
    else:
        return response


@app.route('/contactus')
def user():
    return render_template('contact_us.html')


@app.route('/contactus/save', methods=['POST'])
def contactus_save():
    if request.method == 'POST':
        fname = request.form.get("fname")
        email = request.form.get("email")
        cnum = request.form.get("cnum")
        subject = request.form.get("subject")
        message = request.form.get("message")
        date = request.form.get("date")
        dict = {"name": fname, "email": email, "contact": cnum, "subject": subject, "message": message, "date": date }
        conn_contact = dbconnection.db["contact_messages"]
        conn_contact.insert_one(dict)
        return " SUCCESSFULY ENTERED! "

if __name__ == '__main__':
    toastr.init_app(app)
    app.run()
