from bottle import get, post, default_app

import git

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
    return "xxaxaxxx"

application = default_app()
