from flask import request, render_template
import dbconnection


def get_courses_page():
    collection_name = dbconnection.db["courses"]
    course_list = collection_name.find()
    return render_template("course.html", course_list=course_list)


def get_course_application_page():
    return render_template('admission.html')


def apply_course():
    stname = request.form.get("stname")
    fname = request.form.get("fname")
    mname = request.form.get("mname")
    email = request.form.get("email")
    phno = request.form.get("phno")
    gender = request.form.get("gender")
    higdgr = request.form.get("higdgr")
    appfr = request.form.get("appfr")
    dict = {"Student Name": stname, " Father's Name": fname, "Mother's Name": mname, "Email": email,
            "Phone NUmber": phno, "Gender": gender, "Highest Degree": higdgr, "Apply For": appfr}
    conn_contact = dbconnection.db["admission_applications"]
    conn_contact.insert_one(dict)
    return " CONGRS!!!! Your name registered for this course Successfully"
