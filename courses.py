from bson import ObjectId
from flask import request, render_template, flash, redirect
import dbconnection
import course_category
import admin_courses


def get_courses_page():
    course_category_list = course_category.get_course_categories()
    collection_name = dbconnection.db["courses"]
    for course_category_item in course_category_list:
        if course_category_item['category_code'] == 1:
            query = {'course_category_id': course_category_item['_id']}

            health_sci_course_list = collection_name.find(query)

        elif course_category_item['category_code'] == 2:
            query = {'course_category_id': course_category_item['_id']}
            infor_tech_course_list = collection_name.find(query)

        elif course_category_item['category_code'] == 3:
            query = {'course_category_id': course_category_item['_id']}
            business_course_list = collection_name.find(query)

    return render_template("course.html", health_sci_course_list=health_sci_course_list,
                           infor_tech_course_list=infor_tech_course_list, business_course_list=business_course_list,
                           title="Courses")


def get_course_application_page(course_id):
    try:
        course_list = admin_courses.get_all_courses()
        course_details = admin_courses.get_course_details_by_id(course_id)
        return render_template("admission.html", course_list=course_list, course_details=course_details,
                               selected_course_id=course_id, title="Course Application")
    except Exception as e:
        print(e)
        flash("Error occurred. Please try again!", 'error')
        return redirect('/courses')


def apply_course():
    try:
        stname = request.form.get("stname")
        fname = request.form.get("fname")
        mname = request.form.get("mname")
        email = request.form.get("email")
        phno = request.form.get("phone")
        gender = request.form.get("gender")
        higdgr = request.form.get("hdegree")
        course_id = request.form.get("course_id")
        dict = {"student_name": stname, " father_name": fname, "mother_name": mname, "email": email,
                "phone_number": phno, "gender": gender, "highest_degree": higdgr, "course_id": ObjectId(str(course_id))}
        conn_contact = dbconnection.db["admission_applications"]
        conn_contact.insert_one(dict)
        flash("You have applied successfully.", 'success')
    except Exception as e:
        print(e)
        flash("Error occurred. Please try again!", 'error')

    return redirect('/courses')
