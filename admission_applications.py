from bson import ObjectId
from flask import render_template, flash, redirect
import dbconnection
import admin_courses


def get_admission_application_by_course_and_email(course_id, email):
    query = {'course_id': course_id, 'email': email}
    collection_name = dbconnection.db["admission_applications"]
    return collection_name.find_one(query)


def get_pending_admission_applications_page():
    try:
        pending_applications_list = get_pending_admission_applications()
        return render_template("admin_admission_applications.html", pending_applications_list=pending_applications_list,
                               title='Admission Applications')
    except Exception as e:
        print(e)
        flash("Error occurred. Please try again!", 'error')
        return redirect('/admin/courses')


def get_pending_admission_applications():
    application_status_coll = dbconnection.db["application_status"]
    decided_applications_id = application_status_coll.find()
    decided_applications_id_list = []

    for decided_applications in decided_applications_id:
        decided_applications_id_list.append(decided_applications['application_id'])

    admission_applications_collection = dbconnection.db["admission_applications"]
    pending_applications_query = {'_id': {'$nin': decided_applications_id_list}}
    pending_applications = admission_applications_collection.find(pending_applications_query)

    pending_applications_list = []

    for application in pending_applications:
        course_details = admin_courses.get_course_details_by_id(application['course_id'])
        application['course_details'] = course_details
        pending_applications_list.append(application)

    return pending_applications_list


def get_application_by_id(application_id):
    try:
        query = {'_id': ObjectId(str(application_id))}
        collection_name = dbconnection.db["admission_applications"]
        application_details = collection_name.find_one(query)
        return render_template("admin_admission_applications_view.html", application_details=application_details,
                               title='Admission Application')
    except Exception as e:
        print(e)
        flash("Error occurred. Please try again!", 'error')
        return redirect('/admin/admission/applications')
