import sqlite3

connection = sqlite3.connect("courses.db")
cursor = connection.cursor()

cursor.execute("PRAGMA foreign_keys = ON")

cursor.execute("CREATE TABLE IF NOT EXISTS courses(courseID INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT NOT NULL, teacher TEXT NOT NULL, credits INTEGER NOT NULL, semester INTEGER NOT NULL)")