import os
import re

import smtplib
from cs50 import SQL
from random import randint
from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    # Show list of users' table numbers
    if request.method == "GET":
        # # Checks if the user's time difference is less than 30 min, if not delete the table
        # time = db.execute("SELECT CURRENT_TIME")
        # time1 = int(time[0]["CURRENT_TIME"].replace(":", ""))
        # oldTime = db.execute("SELECT time FROM users WHERE id = :id", id=session["user_id"])
        # if oldTime[0]["time"] is not None:
        #     oldTime = int(oldTime[0]["time"].replace(":", ""))
        #     if ((time1 / 10000) % 10) != ((oldTime / 10000) % 10):
        #         if time1 - oldTime > 7000:
        #             db.execute("UPDATE users SET tab = NULL, time = NULL WHERE id = :id", id=session["user_id"])
        #     else:
        #         if time1 - oldTime > 3000:
        #             db.execute("UPDATE users SET tab = NULL, time = NULL WHERE id = :id", id=session["user_id"])

        # # Create list of friends
        # friends = []
        # other = db.execute("SELECT * FROM friends WHERE userid1 = :userID", userID=session["user_id"])
        # for elem in other:
        #     friends.append(elem["userid2"])
        # other2 = db.execute("SELECT * FROM friends WHERE userid2 = :userID", userID=session["user_id"])
        # for elem in other2:
        #     friends.append(elem["userid1"])
        # users = []
        # for num in friends:
        #     temp = db.execute("SELECT * FROM users WHERE id = :userID", userID=num)
        #     if temp[0]["tab"] is not None:
        #         users.append(temp[0])

        # # Checks if the user's time difference is less than 30 min, if not delete the table
        # for user in users:
        #     oldTime = db.execute("SELECT time FROM users WHERE id = :id", id=user["id"])
        #     if oldTime[0]["time"] is not None:
        #         oldTime = int(oldTime[0]["time"].replace(":", ""))
        #         if ((time1 / 10000) % 10) != ((oldTime / 10000) % 10):
        #             if time1 - oldTime > 7000:
        #                 db.execute("UPDATE users SET tab = NULL, time = NULL WHERE id = :id", id=user["id"])
        #         else:
        #             if time1 - oldTime > 3000:
        #                 db.execute("UPDATE users SET tab = NULL, time = NULL WHERE id = :id", id=user["id"])

        # # Create list of friends in Annenberg at the moment
        # usersReal = []
        # for num in friends:
        #     temp = db.execute("SELECT * FROM users WHERE id = :userID", userID=num)
        #     if temp[0]["tab"] is not None:
        #         usersReal.append(temp[0])

        # Get all the information about the user himself
        you = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])
        you[0]["tab"] = "Not in Annenberg"
        your_table = db.execute("SELECT tab FROM users WHERE id = :id", id=session["user_id"])
        if your_table[0]["tab"] is not None:

            you = db.execute("SELECT * FROM users WHERE id = :id", id=session["user_id"])

    # Let user manually leave Annenberg with a button
    else:
        if request.form.get("b1") == "1":
            db.execute("UPDATE users SET tab = NULL, time = NULL WHERE id = :id", id=session["user_id"])
            return redirect("/")

    return render_template("index.html", users=usersReal, you=you)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    # Enter table number
    if request.method == "POST":
        # Get table from form input
        tab = request.form.get("table")
        # Make sure user input is valid
        if not tab:
            return apology("must provide tab", 400)
        x = db.execute("UPDATE users SET tab = :tab WHERE id = :userid",
                       userid=session["user_id"], tab=tab)
        y = db.execute("UPDATE users SET time = CURRENT_TIME WHERE id = :userid",
                       userid=session["user_id"])
        # Redirect user to home page
        return redirect("/")

    # If the method is GET, return enter table page
    else:
        return render_template("buy.html")


@app.route("/check", methods=["GET"])
def check():
    # Return true if username available, else false, in JSON format
    # Make sure that the user inputs username
    username = request.args.get("username")
    if not username:
        return jsonify(False)
    # Make sure username is in database
    rows = db.execute("SELECT * FROM users WHERE username = :name", name=username.lower())
    if len(rows) > 0:
        return jsonify(False)
    return jsonify(True)


@app.route("/login", methods=["GET", "POST"])
def login():
    # Log user in
    # Forget any user_id
    session.clear()
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted`
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username").lower())

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
    # Log user out

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure email was submitted
        if not request.form.get("email"):
            return apology("must provide email", 400)
        # Ensure password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 400)
        # Ensure confirmation was submitted
        if not request.form.get("confirmation"):
            return apology("must confirm password", 400)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 400)
        if not request.form.get("fullname"):
            return apology("must provide full name", 400)

         # Query database to see if the email is taken
        rows2 = db.execute("SELECT * FROM users WHERE email = :email", email=request.form.get("email"))
        if rows2:
            return apology("Sorry, this email is already taken!")
        # Query database to see if username is taken
        rows = db.execute("SELECT * FROM users WHERE username = :name", name=request.form.get("username").lower())
        if rows:
            return apology("Sorry, this username is already taken!")

        # Check that the email is ...@college.harvard.edu
        regex = '[_a-z0-9-]+(\.[_a-z0-9-]+)*@college.harvard.edu'
        email = request.form.get("email")
        match = re.match(regex, email)
        if match == None:
            return apology("you should use @college.harvard.edu email", 400)

        # Generate a random number as a verification code and put it into the database
        key = randint(1000, 9999)
        insert = db.execute("INSERT INTO ver (email, code, username, hash, fullname) VALUES (:email, :code, :username,:hash,:fullname)",
                            email=email, code=key, username=request.form.get("username").lower(), hash=generate_password_hash(request.form.get("password")), fullname=request.form.get("fullname"))

        # Email the user
        to = email
        gmail_user = 'iceberg.friends@gmail.com'
        gmail_pwd = '12345678ice'
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo()
        smtpserver.login(gmail_user, gmail_pwd)
        header = 'To:' + to + '\n' + 'From: ' + gmail_user + '\n' + 'Subject:Iceberg Verification \n'
        msg = header + '\n Your access code for Iceberg is: \n\n' + str(key)
        smtpserver.sendmail(gmail_user, to, msg)
        smtpserver.quit()

        # Redirect user to a page to enter the verification code
        return redirect("/verify")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("register.html")


@app.route("/verify", methods=["GET", "POST"])
def verify():
    # Check the code from the database
    if request.method == "POST":
        e = request.form.get("email")
        info = db.execute("SELECT * FROM ver WHERE email = :email", email=e)
        if info != [] and str(request.form.get("code")) == str(info[0]["code"]):
            # Insert new user info in database
            insert = db.execute("INSERT INTO users (username, hash, fullname, email) VALUES (:username,:hash, :fullname, :email)",
                                username=info[0]["username"].lower(), hash=info[0]["hash"], fullname=info[0]["fullname"], email=request.form.get("email"))
            # Get id from the username
            rows = db.execute("SELECT id FROM users WHERE username = :username",
                              username=info[0]["username"].lower())
            # Remember which user has logged in
            session["user_id"] = rows[0]["id"]
            # Delete the verification code from the database
            db.execute("DELETE FROM ver WHERE code = :code", code=str(request.form.get("code")))
            return redirect("/")
        else:
            # If the verification code is incorrect, prompt the user to try again
            return redirect("/verifyAgain")

    else:
        return render_template("verify.html")


@app.route("/verifyAgain", methods=["GET", "POST"])
def verifyAgain():
    # Informs user that the verification code is incorrect, so they can try again
    if request.method == "POST":
        return redirect("/verify")
    else:
        return render_template("verify_again.html")


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    # Add friend
    if request.method == "POST":
        # Get friend's username
        friendname = request.form.get("friendname")
        if not friendname:
            return apology("must provide friend's username", 400)
        friendid = db.execute("SELECT id FROM users WHERE username = :name", name=friendname)
        if not friendid:
            return apology("Sorry, this friend does not exist!")

        # Get friend's id, and check if the users are already friends
        other = db.execute("SELECT * FROM friends WHERE userid1 = :userID", userID=session["user_id"])
        for elem in other:
            if elem["userid2"] == friendid[0]["id"]:
                return apology("Sorry, you are already friends!")
        other2 = db.execute("SELECT * FROM friends WHERE userid2 = :userID", userID=session["user_id"])
        for elem in other2:
            if elem["userid1"] == friendid[0]["id"]:
                return apology("Sorry, you are already friends!")
        # Insert the two new friends' ids into a database that keeps track of friends
        db.execute("INSERT INTO friends (userid1, userid2) VALUES (:userid1,:userid2)",
                   userid1=session["user_id"], userid2=friendid[0]["id"])
        return redirect("/")

    else:
        return render_template("sell.html")


@app.route("/change", methods=["GET", "POST"])
@login_required
def change():
    # Change password
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Make sure username matches
        rows = db.execute("SELECT * FROM users WHERE username = :name", name=request.form.get("username").lower())
        if rows == []:
            return apology("Username not found!")
        if rows[0]["username"].lower() != request.form.get("username").lower():
            return apology("Usernames do not match!")

        # Ensure old password was submitted
        if not request.form.get("oldpassword"):
            return apology("must provide password", 403)
        # Ensure new password was submitted
        if not request.form.get("password"):
            return apology("must provide password", 403)
        # Ensure confirmation was submitted and passwords match
        if not request.form.get("confirmation"):
            return apology("must confirm password", 403)
        if request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        # Update new user info in database
        x = db.execute("UPDATE users SET hash = :hash WHERE id = :userID",
                       userID=session["user_id"], hash=generate_password_hash(request.form.get("password")))
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("change.html")


def errorhandler(e):
    """Handle error"""
    return apology(e.name, e.code)


# listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
