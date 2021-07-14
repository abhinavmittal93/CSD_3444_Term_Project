from flask import Flask, render_template, session, redirect
from flask_toastr import Toastr
import admin_courses
from flask import Flask, request, render_template, session, redirect, flash
import dbconnection

import login
from flask_session import Session
from user import User
import Contact_Us

app = Flask(__name__)
toastr = Toastr(app)
# admin_courses_obj = AdminCourses()


app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)

app.add_url_rule('/login', view_func=login.login_page)
app.add_url_rule('/authenticate', view_func=login.authenticate_admin, methods=['POST'])
app.add_url_rule('/logout', view_func=login.logout)

app.add_url_rule('/admin/courses', view_func=admin_courses.get_all_courses)
app.add_url_rule('/admin/courses/delete/<string:object_id>', endpoint='delete_course', view_func=admin_courses.delete_course)
app.add_url_rule('/admin/course/new', view_func=admin_courses.get_add_new_course_page)
app.add_url_rule('/admin/course/edit/<string:course_id>', endpoint='get_edit_course_page', view_func=admin_courses.get_edit_course_page)
app.add_url_rule('/admin/course/save', view_func=admin_courses.save_course, methods=['POST'])

app.add_url_rule('/contactus', view_func=Contact_Us.get_contact_us_page)
app.add_url_rule('/contactus/save', view_func=Contact_Us.save_contact_us_details, methods=['POST'])


@app.route("/")
def home():
    if not session.get("email"):
        return render_template("home.html", title='Home')
    else:
        collection_name = dbconnection.db["admins"]
        user = collection_name.find_one()
        return render_template("admin_home.html", user=user, title='Home')

@app.route("/add_new_user")
def add_new_user():
    user = User("Abhinav Mittal", "abhinavmittal93@gmail.com", "@Bhinav123")
    response = user.create_new_user(user)
    if (response):
        return 'User created successfully'
    else:
        return response


if __name__ == '__main__':
    toastr.init_app(app)
    app.run()
