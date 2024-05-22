from bottle import get, template, post, request, redirect
import sqlite3 as sql

@get("/signup")
def _():
    con = sql.connect("users.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users")

    rows = cursor.fetchall()
    
    users = []
    
    for row in rows:
      users.append(row)
    
    return template("signup.html", users = users)


@post("/signup")
def _():
  try:
    con = sql.connect("users.db")
    cursor = con.cursor()
    # cursor.execute("DROP TABLE IF EXISTS users")
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        email TEXT,
                        password TEXT,
                        active BOOLEAN,
                        key TEXT,
                        token TEXT,
                        created_at INTEGER DEFAULT (strftime('%s', 'now'))
                        )''')

    cursor = con.cursor()

    email = request.forms.get("email", "")
    password = request.forms.get("password", "")
    
    #TODO hash password

    key = 12345
    active = 0

    #generate token 
    token = 987654321


    cursor.execute("INSERT INTO users (email, password, active, key, token) VALUES (?, ?, ?, ?, ?)",
                   (email, password, active, key, token))
    
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # Print each row
    con.commit()
    con.close()
    return redirect('/verify')
  except Exception as ex:
    print(ex)
    return(ex)

