from bson import ObjectId
from flask import request, render_template, flash, redirect
import dbconnection
import course_category
import admin_courses
import admission_applications
from logconfig import LogConfig

log_config = LogConfig()
logger = log_config.logger_config()


# It gets the courses list on the home page for the user.
def get_courses_page():
    logger.info('get_courses_page() begins')
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


# It gets the application page with the selected the course by the user
def get_course_application_page(course_id):
    logger.info(f'get_course_application_page({course_id}) begins')
    try:
        course_list = admin_courses.get_all_courses()
        course_details = admin_courses.get_course_details_by_id(course_id)
        return render_template("admission.html", course_list=course_list, course_details=course_details,
                               selected_course_id=course_id, title="Course Application")
    except Exception as e:
        print(e)
        logger.error(f'Exception occurred in get_course_application_page({course_id}): {e}')
        flash("Error occurred. Please try again!", 'error')
        return redirect('/courses')


# It gets the course details page for the selected course from the home page
def get_course_view_page(course_id):
    logger.info(f'get_course_view_page({course_id}) begins')
    try:
        course_details = admin_courses.get_course_details_by_id(course_id)
        return render_template("course_view.html", course_details=course_details, title='Course - ' + course_details['course_name'])
    except Exception as e:
        print(e)
        logger.error(f'Exception occurred in get_course_view_page({course_id}): {e}')
        flash("Error occurred. Please try again!", 'error')
        return redirect('/courses')


# It saves the user details in database for a particular course.
# And it validates if the user has already applied for the course or not.
def apply_course():
    logger.info('apply_course() begins')
    try:
        email = request.form.get("email")
        course_id = request.form.get("course_id")
        if admission_applications.get_admission_application_by_course_and_email(ObjectId(str(course_id)), email.lower()) is not None:
            flash("You have already applied to this course. Please check the status in \"Check Application Status\" menu.", 'warning')
            return redirect('/courses')


        stname = request.form.get("stname")
        fname = request.form.get("fname")
        mname = request.form.get("mname")
        phno = request.form.get("phone")
        gender = request.form.get("gender")
        higdgr = request.form.get("hdegree")
        dict = {"student_name": stname, "father_name": fname, "mother_name": mname, "email": email,
                "phone_number": phno, "gender": gender, "highest_degree": higdgr, "course_id": ObjectId(str(course_id))}
        conn_contact = dbconnection.db["admission_applications"]
        conn_contact.insert_one(dict)
        flash("You have applied successfully.", 'success')
    except Exception as e:
        print(e)
        logger.error(f'Exception occurred in apply_course(): {e}')
        flash("Error occurred. Please try again!", 'error')

    return redirect('/courses')
