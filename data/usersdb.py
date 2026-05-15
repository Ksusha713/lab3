import sqlite3
import bcrypt

def db_connection():
    connection = sqlite3.connect("users.db")
    return connection

def create_db():
    connection = db_connection()
    cursor = connection.cursor()
    cursor.execute("PRAGMA foreign_keys = ON")
    cursor.execute("CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")
    connection.commit()
    connection.close()

