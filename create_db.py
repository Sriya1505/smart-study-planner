import sqlite3

conn = sqlite3.connect("database.db")

conn.execute("""
CREATE TABLE users(
username TEXT,
password TEXT
)
""")

conn.execute("""
CREATE TABLE tasks(
id INTEGER PRIMARY KEY AUTOINCREMENT,
user TEXT,
task TEXT,
date TEXT
)
""")

conn.commit()
conn.close()