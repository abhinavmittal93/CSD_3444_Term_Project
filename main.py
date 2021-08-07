from flask_toastr import Toastr
import admin_courses
from flask import Flask, render_template, session, redirect, request
import dbconnection

import courses

import login
from flask_session import Session
import application_status
from user import User
import Contact_Us
import admission_applications

app = Flask(__name__)
toastr = Toastr(app)

# Configuring the app
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
# Uncomment the below line in development mode to check the HTML changes live.
# app.config["TEMPLATES_AUTO_RELOAD"] = True
Session(app)


# Defining all the endpoints
app.add_url_rule('/login', view_func=login.login_page)
app.add_url_rule('/authenticate', view_func=login.authenticate_admin, methods=['POST'])
app.add_url_rule('/logout', view_func=login.logout)

app.add_url_rule('/admin/courses', view_func=admin_courses.get_admin_course_list_page)
app.add_url_rule('/admin/courses/delete/<string:object_id>', endpoint='delete_course', view_func=admin_courses.delete_course)
app.add_url_rule('/admin/course/new', view_func=admin_courses.get_add_new_course_page)
app.add_url_rule('/admin/course/edit/<string:course_id>', endpoint='get_edit_course_page', view_func=admin_courses.get_edit_course_page)
app.add_url_rule('/admin/course/save', view_func=admin_courses.save_course, methods=['POST'])
app.add_url_rule('/admin/admission/applications', view_func=admission_applications.get_pending_admission_applications_page)
app.add_url_rule('/admin/admission/applications/<string:application_id>', endpoint='get_application_by_id', view_func=admission_applications.get_application_by_id)
app.add_url_rule('/admin/admission/application/updatestatus', view_func=admission_applications.update_application_status, methods=['POST'])

app.add_url_rule('/contactus', view_func=Contact_Us.get_contact_us_page)
app.add_url_rule('/contactus/save', view_func=Contact_Us.save_contact_us_details, methods=['POST'])

app.add_url_rule('/courses', view_func=courses.get_courses_page)
app.add_url_rule('/course/apply/<string:course_id>', endpoint='get_course_application_page', view_func=courses.get_course_application_page)
app.add_url_rule('/course/apply/save', view_func=courses.apply_course, methods=['POST'])
app.add_url_rule('/course/<string:course_id>', endpoint='get_course_view_page', view_func=courses.get_course_view_page)

app.add_url_rule('/application/status', view_func=application_status.get_check_application_status_page)
app.add_url_rule('/application/status/check', view_func=application_status.check_application_status, methods=['POST'])


# Home Page endpoint
# It will redirect the user on the basis of its role by checking the session.
@app.route("/")
def home():
    if not session.get("email"):
        return redirect('/courses')
    else:
        collection_name = dbconnection.db["admins"]
        user = collection_name.find_one()
        return render_template("admin_home.html", user=user, title='Home')


# It will check if the user is logged in before every request which contains "/admin" in it.
@app.before_request
def admin():
    endpoint = str(request.url_rule)
    if endpoint.startswith('/admin'):
        if not session.get("email"):
            return redirect('/login')


# Method to create a new user with static info
@app.route("/add_new_user")
def add_new_user():
    user = User("Abhinav Mittal", "abhinavmittal93@gmail.com", "@Bhinav123")
    response = user.create_new_user(user)
    if response:
        return 'User created successfully'
    else:
        return response


# It handles the error 404, in case user tries to open a URL which does not exist.
@app.errorhandler(404)
def handle_page_not_found_error(e):
    return render_template('404.html', title="Page Not Found"), 404


# It handles the error 500, in case there's an unhandled exception occurs.
@app.errorhandler(500)
def handle_internal_server_error(e):
    return render_template('500.html', title="Internal Server Error"), 500


# main method to run the app
if __name__ == '__main__':
    toastr.init_app(app)
    app.run()
