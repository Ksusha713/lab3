import sqlite3
import bcrypt

connection = sqlite3.connect("users.db")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("CREATE TABLE IF NOT EXISTS users(userID INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT UNIQUE NOT NULL, password TEXT NOT NULL)")

