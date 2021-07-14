import dbconnection

def get_course_categories():
    collection_name = dbconnection.db["course_category"]
    return collection_name.find()