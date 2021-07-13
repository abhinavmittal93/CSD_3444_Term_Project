from flask import request, render_template, redirect, flash
import dbconnection


def get_contact_us_page():
    return render_template('contact_us.html')


def save_contact_us_details():
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
    except:
        flash('An error occured. Please try again.', 'error')
    return redirect('/contactus')
