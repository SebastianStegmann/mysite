from bottle import get, post, default_app, run, template, request
import json
import git
import sqlite3 as sql

# https://GITHUB-TOKEN-HERE@github.com/GITUHB-USERNAME/mysite.git

##############################
@post('/secret')
def git_update():
  repo = git.Repo('./mysite')
  origin = repo.remotes.origin
  repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
  origin.pull()
  return ""

@get("/")
def _():
    return "Crime server"

@get("/signup")
def _():
    con = sql.connect("users.db")
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users")

    rows = cursor.fetchall()
    
    return template("signup.html", users = "Hej")


@post("/signup")
def _():
    con = sql.connect("users.db")
    cursor = con.cursor()
    # cursor.execute("DROP TABLE IF EXISTS criminals")
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
    active = False 

    #generate token 
    token = 1


    cursor.execute("INSERT INTO users (email, password, active, key, token) VALUES (?, ?, ?, ?, ?)",
                   (email, password, active, key, token))
    
    cursor = con.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # Print each row
    con.commit()
    con.close()
    return json.dumps(rows)

try:
  import production
  application = default_app()
except Exception as ex:
  print("Running local server")
  run(host="127.0.0.1", port=80, debug=True, reloader=True)
