import dbconnection

def get_admission_application_by_course_and_email(course_id, email):
    query = {'course_id': course_id, 'email': email}
    collection_name = dbconnection.db["admission_applications"]
    return collection_name.find_one(query)