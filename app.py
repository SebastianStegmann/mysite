from bottle import get, post, default_app, run, template, request, redirect
import json
import git
import sqlite3 as sql
import routes.verify
import routes.get_token
import routes.signup

# https://GITHUB-TOKEN-HERE@github.com/GITUHB-USERNAME/mysite.git

###############################
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

try:
  import production
  application = default_app()
except Exception as ex:
  print("Running local server")
  run(host="127.0.0.1", port=1234, debug=True, reloader=True)
