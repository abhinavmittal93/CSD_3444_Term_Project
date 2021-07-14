from bson import ObjectId
from flask import render_template, request, redirect, flash, session
import dbconnection
from login_required_decorator import login_required


@login_required
def get_all_courses():
    try:
        collection_name = dbconnection.db["courses"]
        course_list = collection_name.find()
        return render_template("course.html", course_list = course_list, title ='course')
    except:
        flash("Try again!! Error occured", 'error')
        return render_template("course.html", course_list =None)

def get_course_detail_by_id(course_id):
    query= {'_id': ObjectId(course_id)}
    collection_name = dbconnection.db["courses"]
    return collection_name.find_one(query)


