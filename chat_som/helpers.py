import csv
import datetime
import pytz
import requests
import subprocess
import urllib
import uuid
import re

from flask import redirect, render_template, session
from functools import wraps


def apology(message, code=400):
    """Render message as an apology to user."""

    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [
            ("-", "--"),
            (" ", "-"),
            ("_", "__"),
            ("?", "~q"),
            ("%", "~p"),
            ("#", "~h"),
            ("/", "~s"),
            ('"', "''"),
        ]:
            s = s.replace(old, new)
        return s

    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/0.12/patterns/viewdecorators/
    """

    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)

    return decorated_function


# Define password criteria
def validate_password(password):
    # Initialize Counts based upon criteria
    count_letters = 0
    count_numbers = 0
    count_special = 0

    # Check password against criteria
    for character in password:
        if character.isalpha():
            count_letters += 1
        elif character.isdigit():
            count_numbers += 1
        elif re.match("[!@#$%^&*(),.?\":{}|<>]", character):
            count_special += 1
    # Check for minimum criteria compliance
    if count_letters >= 2 and count_numbers >= 2 and count_special >= 2:
        return True
    else:
        return False
