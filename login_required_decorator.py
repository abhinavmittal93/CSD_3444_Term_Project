import functools

from flask import session, redirect, url_for, request


def login_required():
    if "email" not in session or session.get("email") == '':
        return redirect(url_for("login_page"))
