import os
import sqlite3
import csv
import pandas as pd
import numpy as np
import openai
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, validate_password

from datetime import datetime

# Configure application
app = Flask(__name__)

# import chat.py
import chat

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Define connection to allow multipule users
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


#Define Database "somchatusers.db"
DATABASE = 'somchatusers.db'

# Connect to SQLite Database "somchatusers.db"
conn = sqlite3.connect(DATABASE)
conn.row_factory = sqlite3.Row # enables column access by name: row['column_name']

# Create cursor object
cursor = conn.cursor()

# Execute SQL commands
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    username TEXT NOT NULL,
    hash TEXT NOT NULL,
    cash NUMERIC NOT NULL DEFAULT 10000.00
);
""")
cursor.execute("""
CREATE UNIQUE INDEX IF NOT EXISTS username ON users (username);
""")

# Commit changes and close connection
# conn.commit()
# conn.close()

@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show chat window"""
    # For the current session
    user_id = session["user_id"]

    # Render HTML page for display
    return render_template("index.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE username = ?", (request.form.get("username"),))
            rows = cur.fetchall()
        finally:
            conn.close()

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")



@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")



@app.route("/register", methods=["GET", "POST"])

def register():
    """Register user"""
    # Go to register page if not registered
    if request.method == "GET":
        return render_template("register.html")

    # If registering, pull user inputs from Register.HTML
    else:
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Return apology if usernmae blank
        if not username:
            return apology("Please provide a username to continue.")

        # Return apology if password blank
        if not password:
            return apology("Please provide a password to continue.")

        # Return apology if password confirmation blank
        if not confirmation:
            return apology("Please confirm your password to continue.")

        # Return apology if password and confirmation do not match
        if password != confirmation:
            return apology("Password and Password Confirmation do not match. Please try again.")

        # Check for password creation criteria (extra personalized touch)
        if not validate_password(password):
            return apology("Password does not meet the minimum requirements. Please include at least 2 letters, 2 numbers, and 2 symbols.")

        # Generate password hash for security
        hash = generate_password_hash(password)

    # Insert user into database
    try:
        # Insert username and has into database
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO users (username, hash) VALUES (?, ?)", (username, hash))
        conn.commit() # commit the transaction
        new_id = cur.lastrowid
    except sqlite3.IntegrityError:
        # Return apology if username already exsits
        return apology("Try again. Username already exists.")
    finally:
        conn.close()

        # Establish a new session
        session["user_id"] = new_id
        return redirect("/")

@app.route('/course_list')
@login_required
def course_list():
    # For the current session
    user_id = session["user_id"]
    
    try:
        # Read the CSV file into a DataFrame and then convert to a list of dictionaries
        df = pd.read_csv("course_list/courseslist.csv")
        courses = df.to_dict(orient='records')
    except FileNotFoundError as e:
        print(f"Error: {e}")  # Log the error for debugging
        return apology("Course list is not found")

    for course in courses:
        course["course_id"] = course["Course ID"]
        course["course_number"] = course["Course Number"]  
        course["course_title"] = course["Course Title"]
        course["units"] = course["Units"]    
        course["times"] = course["Daytimes"]
        course["course_id"] = course["Course ID"] 
        course["faculty"] = course["Faculty 1"]    
        course["room"] = course["Room"]    
        course["section"] = course["Section"]    
        course["syllabus"] = course["Syllabus"]       
        course["old_syllabus"] = course["Old Syllabus"]  
    return render_template('course_list.html', courses=courses)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/send_prompt', methods=['GET', 'POST'])
def send_prompt():
    response = ""
    if request.method == 'POST':
        user_prompt = request.form['prompt']
        # Call the function to get the response from GPT
        response = get_gpt_response(user_prompt)  # Replace with your function to get the GPT response

    return render_template('index.html', response=response)
