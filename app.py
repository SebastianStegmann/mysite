from bottle import get, post, default_app, run, template, request, redirect, response
import json
import git
import routes.get_token
import routes.signup
import routes.index
import routes.verify
import routes.truncate
import sqlite3 as sql

# https://GITHUB-TOKEN-HERE@github.com/GITUHB-USERNAME/mysite.git

###############################
@post('/secret')
def git_update():
  repo = git.Repo('./mysite')
  origin = repo.remotes.origin
  repo.create_head('main', origin.refs.main).set_tracking_branch(origin.refs.main).checkout()
  origin.pull()
  return ""

@post('/update-crime')
def _():
    
    token = request.forms.get("token", "")
    
    if token == None:
      response.type = 400
      return {"Error": "No token included"}
    
    con = sql.connect("users.db")
    cursor = con.cursor()
    
    cursor.execute('SELECT active FROM users WHERE token = ?', (token,))
    
    active = cursor.fetchone()
    
    if active is None or active[0] != True:
        response.type = 400
        return {"Error": "Account is not active or not found"}

    # Read data from JSON file
    with open('crimes.json', 'r') as file:
        data = json.load(file)
    # Set response content type to JSON
    response.content_type = 'application/json'
    # Convert dictionary to JSON string
    json_data = json.dumps(data)

    # Set CORS headers
    response.headers['Access-Control-Allow-Origin'] = '*'  # Allow requests from any origin
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'  # Allow GET requests and preflight OPTIONS requests
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'  # Allow these headers


    if data == None:
      response.type = 400
      return {"Error": "no such data"}

    response.type = 200
    return json_data


try:
  import production
  application = default_app()
except Exception as ex:
  print("Running local server")
  run(host="127.0.0.1", port=1233, debug=True, reloader=True)
