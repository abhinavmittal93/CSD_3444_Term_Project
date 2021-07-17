from bson import ObjectId
from flask import request, render_template, redirect, flash
import dbconnection


def get_check_application_status_page():
    return render_template("application_status_check.html", title="Check Application Status")


def check_application_status():
    email = request.form["email"]
    query = {'email': email.lower()}
    collection_name = dbconnection.db["application_status"]

    status_records = collection_name.find(query)
    if not status_records:
        flash("No record found.", 'error')
        return redirect('/application/status')
    else:
        result_list = []
        for record in status_records:
            application_details = get_application_details(record['application_id'])
            record['application_details'] = application_details

            course_details = get_course_details(ObjectId(str(application_details['course_id'])))
            record['course_details'] = course_details
            result_list.append(record)

        return render_template("application_status.html", status_records=result_list, email=email.lower())


def get_application_details(application_id):
    query = {'_id': application_id}
    collection_name = dbconnection.db["admission_applications"]
    return collection_name.find_one(query)


def get_course_details(course_id):
    query = {'_id': course_id}
    collection_name = dbconnection.db["courses"]
    return collection_name.find_one(query)