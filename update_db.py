import sqlite3

conn = sqlite3.connect('database.db')
c = conn.cursor()

# Drop old table if it exists
c.execute("DROP TABLE IF EXISTS ideas")

# Create new table with correct columns
c.execute('''
    CREATE TABLE ideas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT,
        topic TEXT,
        idea TEXT,
        contact TEXT
    )
''')

conn.commit()
conn.close()

print("Table 'ideas' has been created successfully in database.db.")