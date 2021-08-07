from flask import request, render_template, redirect, flash
import dbconnection
from logconfig import LogConfig

log_config = LogConfig()
logger = log_config.logger_config()


# Gets the contact us page
def get_contact_us_page():
    logger.info('get_contact_us_page() begins')
    return render_template('contact_us.html')


# It saves the details entered by the user on the contact us page.
def save_contact_us_details():
    logger.info('save_contact_us_details() begins')
    try:
        fname = request.form.get("fname")
        email = request.form.get("email")
        cnum = request.form.get("cnum")
        subject = request.form.get("subject")
        message = request.form.get("message")
        date = request.form.get("date")
        contact_message_details = {"name": fname, "email": email.lower(), "contact": cnum, "subject": subject,
                                   "message": message, "date": date}
        conn_contact = dbconnection.db["contact_messages"]
        conn_contact.insert_one(contact_message_details)
        flash('Thanks for contacting us.', 'success')
    except Exception as e:
        logger.error(f'Exception occurred in save_contact_us_details(): {e}')
        flash('An error occured. Please try again.', 'error')
    return redirect('/contactus')
