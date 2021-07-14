from bson import ObjectId
from flask import render_template, request, redirect, flash, session
import dbconnection
from login_required_decorator import login_required
import course_category


@login_required
def get_all_courses():
    try:
        collection_name = dbconnection.db["courses"]
        courses_list = collection_name.find()
        return render_template("admin_courses.html", courses_list=courses_list, title='Courses')
    except Exception as e:
        print(e)
        flash("Error occurred. Please try again!", 'error')
        return render_template("admin_courses.html", courses_list=None)


# @login_required
def delete_course(object_id):
    try:
        collection_name = dbconnection.db["courses"]
        result = collection_name.delete_one({'_id': ObjectId(object_id)})
        flash("Course Deleted Successfully.", 'success')
    except Exception as e:
        print(e)
        flash("Error occurred. Please try again!", 'error')

    return redirect('/admin/courses')


def get_add_new_course_page(course_details={}):
    try:
        course_category_list = course_category.get_course_categories()
        return render_template("admin_course_details.html", course_category_list=course_category_list, course_details=course_details,
                               title="New Course")
    except Exception as e:
        print(e)
        flash("Error occurred. Please try again!", 'error')
        return redirect('/admin/courses')


def get_edit_course_page(course_id):
    try:
        course_category_list = course_category.get_course_categories()
        course_details = get_course_details_by_id(course_id)
        return render_template("admin_course_details.html", course_category_list=course_category_list,
                               course_details=course_details, title="Edit Course")
    except Exception as e:
        print(e)
        flash("Error occurred. Please try again!", 'error')
        return redirect('/admin/courses')


def get_course_details_by_id(course_id):
    query = {'_id': ObjectId(course_id)}
    collection_name = dbconnection.db["courses"]
    return collection_name.find_one(query)


def save_course():
    req = request.form

    course_id = request.form["course_id"]
    course_code = request.form["course_code"]
    course_name = request.form["course_name"]
    course_description = request.form["course_details"]
    course_duration = request.form["course_duration"]
    course_fees = request.form["course_fees"]

    is_co_op_available = False
    if request.form["is_co_op_available"] == 'on':
        is_co_op_available = True

    may_intake = request.form["may_intake"] if "may_intake" in request.form else ''
    sept_intake = request.form["sept_intake"] if "sept_intake" in request.form else ''
    jan_intake = request.form["jan_intake"] if "jan_intake" in request.form else ''

    intakes_available = []
    if may_intake == 'on':
        intakes_available.append('MAY')
    if sept_intake == 'on':
        intakes_available.append('SEPT')
    if jan_intake == 'on':
        intakes_available.append('JAN')

    admission_requirements = request.form["admission_requirements"]
    course_category_id = request.form["course_category_id"]

    course = AdminCourses(course_code, course_name, course_description, course_duration, course_fees,
                          is_co_op_available, intakes_available, admission_requirements, course_category_id)

    missing = list()

    for k, v in req.items():
        if v == "" and k != 'course_id':
            missing.append(k)

    if missing:
        missing_fields_message = f"Missing fields for {', '.join(missing)}"
        flash(missing_fields_message, 'warning')
        return get_add_new_course_page(course)

    try:
        if course_id:
            update_course_details_by_id(course, course_id)
            flash("Course updates successfully!", 'success')
        else:
            save_course_details(course)
            flash("Course added successfully!", 'success')
        return redirect('/admin/courses')
    except Exception as e:
        print(e)
        flash('An error occurred. Please try again!', 'error')
        if course_id:
            return get_edit_course_page(course_id)
        else:
            return get_add_new_course_page(course)


def save_course_details(AdminCourses):
    collection_name = dbconnection.db["courses"]
    record = {"course_code": AdminCourses.course_code,
              "course_name": AdminCourses.course_name,
              "course_description": AdminCourses.course_description,
              "course_duration": AdminCourses.course_duration,
              "course_fees": AdminCourses.course_fees,
              "is_co_op_available": AdminCourses.is_co_op_available,
              "intakes_available": AdminCourses.intakes_available,
              "admission_requirements": AdminCourses.admission_requirements,
              "course_category_id": AdminCourses.course_category_id
              }
    response = collection_name.insert_one(record)
    return response.acknowledged


def update_course_details_by_id(AdminCourses, course_id):
    collection_name = dbconnection.db["courses"]
    record = {"course_code": AdminCourses.course_code,
              "course_name": AdminCourses.course_name,
              "course_description": AdminCourses.course_description,
              "course_duration": AdminCourses.course_duration,
              "course_fees": AdminCourses.course_fees,
              "is_co_op_available": AdminCourses.is_co_op_available,
              "intakes_available": AdminCourses.intakes_available,
              "admission_requirements": AdminCourses.admission_requirements,
              "course_category_id": AdminCourses.course_category_id
              }
    response = collection_name.update_one({"_id": ObjectId(str(course_id))}, {"$set": record})
    return response.acknowledged


class AdminCourses:

    def __init__(self, course_code='', course_name='', course_description='', course_duration='',
                 course_fees=0, is_co_op_available=False, intakes_available='', admission_requirements='',
                 course_category_id=0):
        self.course_code = course_code
        self.course_name = course_name
        self.course_description = course_description
        self.course_duration = course_duration
        self.course_fees = course_fees
        self.is_co_op_available = is_co_op_available
        self.intakes_available = intakes_available
        self.admission_requirements = admission_requirements
        self.course_category_id = course_category_id
