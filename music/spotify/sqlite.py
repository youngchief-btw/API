import sqlite3

con = sqlite3.connect("spotify.db")
con.execute('''CREATE TABLE IF NOT EXISTS spotify
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                value TEXT NOT NULL);''')

def read(name: str):
    cur = con.execute("SELECT value FROM spotify WHERE name = ?", (name,))
    value = cur.fetchone()
    if value:
        return value[0]
    return None


def set(name: str, value: str) -> str:
    if read(name):
        con.execute(f"UPDATE spotify SET value = ? WHERE name = ?", (value, name))
        con.commit()
        return "Updated"
    else:
        con.execute("INSERT INTO spotify (name, value) VALUES (?, ?)", (name, value))
        con.commit()
        return "Created"