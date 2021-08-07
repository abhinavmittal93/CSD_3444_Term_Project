import dbconnection
from logconfig import LogConfig

log_config = LogConfig()
logger = log_config.logger_config()

# It gets the course categories defined in the database
def get_course_categories():
    logger.info('get_course_categories() begins')
    collection_name = dbconnection.db["course_category"]
    return collection_name.find()