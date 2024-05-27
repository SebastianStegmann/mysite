from bottle import get, response, post, request
import smtplib, ssl, json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sqlite3 as sql
import os


def send_email(receiver_email):
  try:
    # return request.json
    email = str(request.json['email'])
    con = sql.connect("mysite/users.db")

    cursor = con.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    if user == None:
        return "no users with that name"

    con.commit()
    con.close()
    sender_email = "billestegmann@gmail.com"
    password = "gghqsdohnpnxqyev"
    receiver_email = user[1]

    message = MIMEMultipart("alternative")
    message["Subject"] = "multipart test"
    message["From"] = sender_email
    message["To"] = receiver_email

    # Create the plain-text and HTML version of your message
    text = f"""\
    Hey Buddy, heres your activation key
    {user[4]}"""
    html = f"""\
    <html>
    <body>
    <p>Hey Buddy, heres your activation key<br>
       <br>
     {user[4]}
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
    response.type = 200

    os._exit(0)
    return json.dumps({"info":"mail sent"})
  except Exception as Ex:
    response.type = 400
    response.content_type = 'application/json'
    return json.dumps({"error":Ex})
