import sqlite3

db = sqlite3.connect(':memory:')
cur = db.cursor()

cur.execute("PRAGMA foreign_keys = 1")

cur.execute("CREATE TABLE posts (id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("CREATE TABLE emps (id INTEGER PRIMARY KEY, f TEXT, i TEXT, tel TEXT, p_id INTEGER, FOREIGN KEY(p_id) REFERENCES posts(id))")
cur.execute("CREATE TABLE clis (id INTEGER PRIMARY KEY, org TEXT, tel TEXT)")
cur.execute("CREATE TABLE ords (id INTEGER PRIMARY KEY, c_id INTEGER, e_id INTEGER, money REAL, dt TEXT, ok INT, FOREIGN KEY(c_id) REFERENCES clis(id), FOREIGN KEY(e_id) REFERENCES emps(id))")

cur.executemany("INSERT INTO posts (name) VALUES (?)", [('Шеф',), ('Раб',)])
cur.executemany("INSERT INTO clis (org, tel) VALUES (?,?)", [('АБВ', '11'), ('ГДЕ', '22')])
cur.executemany("INSERT INTO emps (f, i, tel, p_id) VALUES (?,?,?,?)", [('Петров', 'Пётр', '01', 1), ('Иванов', 'Иван', '02', 2)])
cur.executemany("INSERT INTO ords (c_id, e_id, money, dt, ok) VALUES (?,?,?,?,?)", [(1, 2, 5000, '2024-01-01', 1), (2, 2, 100, '2024-01-02', 0)])


cur.execute("SELECT f, i FROM emps")
print(cur.fetchall())

cur.execute("SELECT org FROM clis")
print(cur.fetchall())

cur.execute("SELECT id, money FROM ords WHERE money > 1000")
print(cur.fetchall())


f_val = 'Петров'
cur.execute("SELECT * FROM emps WHERE f = ?", (f_val,))
print(cur.fetchall())

c_val = 1
cur.execute("SELECT * FROM ords WHERE c_id = ?", (c_val,))
print(cur.fetchall())

p_val = 'Шеф'
cur.execute("SELECT * FROM posts WHERE name = ?", (p_val,))
print(cur.fetchall())

cur.execute("SELECT posts.name, COUNT(emps.id) FROM posts LEFT JOIN emps ON posts.id = emps.p_id GROUP BY posts.name")
print(cur.fetchall())

cur.execute("SELECT clis.org, SUM(ords.money) FROM clis JOIN ords ON clis.id = ords.c_id GROUP BY clis.org")
print(cur.fetchall())

cur.execute("SELECT AVG(money) FROM ords WHERE ok = 1")
print(cur.fetchall())

db.close()
