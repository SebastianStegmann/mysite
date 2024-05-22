from bottle import get, template, post, request, redirect
import sqlite3 as sql

@get("/")
def _():
    return template("index.html")


