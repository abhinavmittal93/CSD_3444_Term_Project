from bson import ObjectId
from flask import render_template, flash, redirect, request
import dbconnection
import admin_courses
import application_status


# Get the application details by email_id and course_id from DB
def get_admission_application_by_course_and_email(course_id, email):
    query = {'course_id': course_id, 'email': email}
    collection_name = dbconnection.db["admission_applications"]
    return collection_name.find_one(query)


# Get the pending applications page
def get_pending_admission_applications_page():
    try:
        pending_applications_list = get_pending_admission_applications()
        return render_template("admin_admission_applications.html", pending_applications_list=pending_applications_list,
                               title='Admission Applications')
    except Exception as e:
        print(e)
        flash("Error occurred. Please try again!", 'error')
        return redirect('/admin/courses')


# Get the application which is neither accepted or rejected, by email id
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


# Get the application details by _id from "admission_applications"
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


# It updates the application status on the basis of admin's decision ('ACCPT' or 'RJCT')
def update_application_status():
    email = request.form["email"]
    status = request.form["status"]
    application_id = request.form["application_id"]
    try:
        application_status.accept_reject_application(email.lower(), status, application_id)
        if status == 'ACCPT':
            flash("Application has been approved successfully.", 'success')
        else:
            flash("Application has been rejected successfully.", 'success')
        return redirect('/admin/admission/applications')
    except Exception as e:
        print(f'An exception occurred while updating the status of an application {e}')
        flash("An error occurred. Please try again.", 'error')
        return redirect('/admin/admission/applications/' + application_id)




