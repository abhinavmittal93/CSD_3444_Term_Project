from bson import ObjectId
from flask import render_template, request, redirect, flash, session
import dbconnection
import course_category
from logconfig import LogConfig

log_config = LogConfig()
logger = log_config.logger_config()


# Get Course List page for Admin
def get_admin_course_list_page():
    logger.info("get_admin_course_list_page() begins")
    try:
        courses_list = get_all_courses()
        return render_template("admin_courses.html", courses_list=courses_list, title='Courses')
    except Exception as e:
        print(e)
        logger.error(f"Exception occurred in get_admin_course_list_page(): {e}")
        flash("Error occurred. Please try again!", 'error')
        return render_template("admin_courses.html", courses_list=None)


# Get all the courses list
def get_all_courses():
    logger.info("get_all_courses() begins")
    collection_name = dbconnection.db["courses"]
    courses_list = collection_name.find()

    result_list = []
    for record in courses_list:
        course_category_details = get_course_category_details(record['course_category_id'])
        record['course_category_details'] = course_category_details
        result_list.append(record)

    return result_list


# Get course category details by _id for the related course
def get_course_category_details(course_category_id):
    logger.info(f"get_course_category_details({course_category_id}) begins")
    query = {'_id': course_category_id}
    collection_name = dbconnection.db["course_category"]
    return collection_name.find_one(query)


# Deletes the course from DB by _id
def delete_course(object_id):
    logger.info(f"delete_course({object_id}) begins")
    try:
        collection_name = dbconnection.db["courses"]
        collection_name.delete_one({'_id': ObjectId(object_id)})
        flash("Course Deleted Successfully.", 'success')
    except Exception as e:
        print(e)
        logger.error(f"Exception occurred in delete_course({object_id}): {e}")
        flash("Error occurred. Please try again!", 'error')

    return redirect('/admin/courses')


# Gets the add new course page for the admin
def get_add_new_course_page(course_details={}):
    logger.info("get_add_new_course_page() begins")
    try:
        course_category_list = course_category.get_course_categories()
        if course_details == {}:
            course_details['intakes_available'] = []
        return render_template("admin_course_details.html", course_category_list=course_category_list,
                               course_details=course_details,
                               title="New Course")
    except Exception as e:
        print(e)
        logger.error(f"Exception occurred in get_add_new_course_page(): {e}")
        flash("Error occurred. Please try again!", 'error')
        return redirect('/admin/courses')


# Gets the add edit course page for the admin
def get_edit_course_page(course_id):
    logger.info(f"get_edit_course_page({course_id}) begins")
    try:
        course_category_list = course_category.get_course_categories()
        course_details = get_course_details_by_id(course_id)
        return render_template("admin_course_details.html", course_category_list=course_category_list,
                               course_details=course_details, title="Edit Course")
    except Exception as e:
        print(e)
        logger.error(f"Exception occurred in get_edit_course_page({course_id}): {e}")
        flash("Error occurred. Please try again!", 'error')
        return redirect('/admin/courses')


# Gets the course details by _id from "courses" collection
def get_course_details_by_id(course_id):
    logger.info(f"get_course_details_by_id({course_id}) begins")
    query = {'_id': ObjectId(course_id)}
    collection_name = dbconnection.db["courses"]
    return collection_name.find_one(query)


# Gets the course details submitted by the admin and saves it
def save_course():
    logger.info("save_course() begins")
    req = request.form

    course_id = request.form["course_id"]
    course_code = request.form["course_code"]
    course_name = request.form["course_name"]
    course_description = request.form["course_details"]
    course_duration = request.form["course_duration"]
    course_fees = request.form["course_fees"]

    is_co_op_available = False
    if "is_co_op_available" in request.form and request.form["is_co_op_available"] == 'on':
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
            flash("Course updated successfully!", 'success')
        else:
            save_course_details(course)
            flash("Course added successfully!", 'success')
        return redirect('/admin/courses')
    except Exception as e:
        print(e)
        logger.error(f"Exception occurred in save_course(): {e}")
        flash('An error occurred. Please try again!', 'error')
        if course_id:
            return get_edit_course_page(course_id)
        else:
            return get_add_new_course_page(course)


# Saves the course details in the DB
def save_course_details(AdminCourses):
    logger.info("save_course_details() begins")
    collection_name = dbconnection.db["courses"]
    record = {"course_code": AdminCourses.course_code,
              "course_name": AdminCourses.course_name,
              "course_description": AdminCourses.course_description,
              "course_duration": AdminCourses.course_duration,
              "course_fees": AdminCourses.course_fees,
              "is_co_op_available": AdminCourses.is_co_op_available,
              "intakes_available": AdminCourses.intakes_available,
              "admission_requirements": AdminCourses.admission_requirements,
              "course_category_id": ObjectId(str(AdminCourses.course_category_id))
              }
    response = collection_name.insert_one(record)
    return response.acknowledged


# It updates the course details by _id
def update_course_details_by_id(AdminCourses, course_id):
    logger.info("update_course_details_by_id() begins")
    collection_name = dbconnection.db["courses"]
    record = {"course_code": AdminCourses.course_code,
              "course_name": AdminCourses.course_name,
              "course_description": AdminCourses.course_description,
              "course_duration": AdminCourses.course_duration,
              "course_fees": AdminCourses.course_fees,
              "is_co_op_available": AdminCourses.is_co_op_available,
              "intakes_available": AdminCourses.intakes_available,
              "admission_requirements": AdminCourses.admission_requirements,
              "course_category_id": ObjectId(str(AdminCourses.course_category_id))
              }
    response = collection_name.update_one({"_id": ObjectId(str(course_id))}, {"$set": record})
    return response.acknowledged


class AdminCourses:

    def __init__(self, course_code='', course_name='', course_description='', course_duration='',
                 course_fees=0, is_co_op_available=False, intakes_available=[], admission_requirements='',
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
