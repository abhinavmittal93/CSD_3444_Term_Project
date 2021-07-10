from flask import render_template, request, redirect, flash, session
import dbconnection
from flask_toastr import Toastr
from login_required_decorator import login_required

toastr = Toastr()


@login_required
def get_all_courses():
    try:
        collection_name = dbconnection.db["courses"]
        courses_list = collection_name.find()
        return render_template("admin_courses.html", courses_list=courses_list)
    except:
        flash("Error occurred. Please try again!", 'error')
        return render_template("admin_courses.html", courses_list=None)


class AdminCourses:

    def __init__(self, course_code='', course_name='', course_description='', course_duration='',
                 course_fees='', is_co_op_available=False, intakes_available=''):
        self.course_code = course_code
        self.course_name = course_name
        self.course_description = course_description
        self.course_duration = course_duration
        self.course_fees = course_fees
        self.is_co_op_available = is_co_op_available
        self.intakes_available = intakes_available

    # @classmethod
    # def add_new_course(cls, course):
    #     collection_name = dbconnection.db["courses"]
    #     record = {"code": course}
    #     response = collection_name.insert_one(record)
    #     return response.acknowledged
