from bottle import get, template, post, request, redirect, HTTPResponse
import sqlite3 as sql
import json
import smtplib, ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import routes.verify


def send_email(receiver_email, key):
    try:
      # Your email sending logic here
      # For brevity, I'm omitting the email sending code
        print('start of send email')
        # email = str(request.json['email'])

        sender_email = "billestegmann@gmail.com"
        password = "gghqsdohnpnxqyev"

        message = MIMEMultipart("alternative")
        message["Subject"] = "multipart test"
        message["From"] = sender_email
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        text = f"""\
        Hey Buddy, heres your activation key
        {key}"""
        html = f"""\
        <html>
        <body>
        <p>Hey Buddy, heres your activation key<br>
           <br>
         {key}
        </p>
        </body>
        </html>
        """

        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        # Create secure connection with server and send email
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(sender_email, password)
            server.sendmail(
            sender_email, receiver_email, message.as_string()
        )
        # If email sent successfully, return True
        return True
    except Exception as Ex:
        # If any error occurs during email sending, return False and the exception information
        return False
        # raise Exception(f"Error sending email:{Ex}")

@get("/signup")
def _():
    try:
        con = sql.connect("~/mysite/users.db")
        cursor = con.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            email TEXT,
                            password TEXT,
                            active BOOLEAN,
                            key TEXT,
                            token TEXT,
                            created_at INTEGER DEFAULT (strftime('%s', 'now'))
                            )''')
        cursor.execute("SELECT * FROM users")

        rows = cursor.fetchall()
        
        users = []
        
        for row in rows:
            users.append(row)
        
        return template("signup.html", users=users)
    except Exception as ex:
        return f"Internal Server Error: {str(ex)}"

@post("/signup")
def _():
    try:
        con = sql.connect("../users.db")
        cursor = con.cursor()

        email = request.forms.get("email", "")
        password = request.forms.get("password", "")

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        existing_user = cursor.fetchone()
        if existing_user:
            # If user already exists, return an error
            raise Exception("Error sending email: user already exists with this email")
        #TODO hash password

        key = 12345
        active = 0

        print('hey')
        #generate token 
        token = 987654321

        cursor.execute("INSERT INTO users (email, password, active, key, token) VALUES (?, ?, ?, ?, ?)",
                       (email, password, active, key, token))

        con.commit()
        con.close()

        # result = send_email(email)

        if send_email(email, key):
            return template("verify")
        else:
            raise Exception({'status': 'Unexpected result from send_email function'})


    except Exception as ex:
        print('Exception occurred:', ex)
        return f"Internal Server Error: {str(ex)}"
