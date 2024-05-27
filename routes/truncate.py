from bottle import post, response, request
import sqlite3 as sql

@post('/truncate')
def _():
  try:
    con = sql.connect("users.db")
    cursor = con.cursor()
    data = request.json
    code = data.get("code","")

    response.content_type = 'application/json'
    if code != "1911771620":
      response.type = 400
      return {"Error": "Wrong code sent"}
    cursor.execute("DELETE FROM users") 
    cursor.close()
    response.type = 200
    return {"Info": "Database was truncated"}
  except Exception as Ex:
    return {"Error": str(Ex)}
