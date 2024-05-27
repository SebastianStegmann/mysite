from bottle import get, post, template, response, request
import sqlite3 as sql
import json

@get('/verify')
def _():
  try:
    return template('verify')
  except Exception as Ex:
    response.type = 400
    return Ex

@post('/verify')
def _():
  try:
    con = sql.connect("users.db")
    cursor = con.cursor()
    email = request.forms.get("email", "")
    key = request.forms.get("key", "")
    
    cursor.execute('''
                  SELECT key, token
                  FROM users
                  WHERE email = ?
                   ''', (email,))
    
    user = cursor.fetchone()

    
    if user is None:
        response.status = 400
        return json.dumps({"error": "User not found"})
        
    if user[0] != key:
        response.status = 400
        return json.dumps({"error": "Invalid password "})

    cursor.execute('''
                      UPDATE users
                      SET active = 1
                      WHERE email = ?
                       ''', (email,))
    con.commit()

    response.content_type = 'application/json'
    return f" Account verified! Nice! Your api token is: {user[1]}"

  except sql.Error as sql_ex:
        response.status = 400
        response.content_type = 'application/json'
        return json.dumps({"error": "Database error", "details": str(sql_ex)})

  except Exception as Ex:
    response.type = 400
    response.content_type = 'application/json'
    return json.dumps({"error": str(Ex)})
