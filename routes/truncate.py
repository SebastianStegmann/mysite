import sqlite3 as sql
from bottle import post, request, response, HTTPResponse

@post('/truncate')
def truncate_database():
    try:
        con = sql.connect("users.db")
        cursor = con.cursor()
        data = request.json
        code = data.get("code", "")

        response.content_type = 'application/json'
        if code != "1911771620":
            raise HTTPResponse(status=400, body={"Error": "Wrong code sent"})

        cursor.execute("DELETE FROM users")
        con.commit()
        cursor.close()
        con.close()

        return {"Info": "Database was truncated"}
    except Exception as Ex:
        return {"Error": str(Ex)}
