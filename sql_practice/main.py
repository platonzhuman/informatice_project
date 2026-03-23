import sqlite3

# Подключение к базе данных
connection = sqlite3.connect("baza.db")
cursor = connection.cursor()

# Создание таблиц (исправлены кавычки)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS `job_titles` (
        `id_job_title` integer primary key NOT NULL UNIQUE,
        `name` TEXT NOT NULL
    );
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS `employees` (
        `id` integer primary key NOT NULL UNIQUE,
        `surname` TEXT NOT NULL,
        `name` TEXT NOT NULL,
        `id_job_title` INTEGER NOT NULL,
        FOREIGN KEY(`id_job_title`) REFERENCES `job_titles`(`id_job_title`)
    );
""")

# Заполнение таблицы job_titles
job_titles_data = [
    (1, 'Менеджер'),
    (2, 'Разработчик'),
    (3, 'Аналитик'),
    (4, 'Дизайнер')
]

cursor.executemany("INSERT OR IGNORE INTO `job_titles` (`id_job_title`, `name`) VALUES (?, ?)", job_titles_data)

# Заполнение таблицы employees
employees_data = [
    (1, 'Иванов', 'Иван', 2),
    (2, 'Петров', 'Петр', 1),
    (3, 'Сидорова', 'Мария', 3),
    (4, 'Козлов', 'Алексей', 2),
    (5, 'Васильева', 'Ольга', 4)
]

cursor.executemany("INSERT OR IGNORE INTO `employees` (`id`, `surname`, `name`, `id_job_title`) VALUES (?, ?, ?, ?)", employees_data)

# Сохранение изменений
connection.commit()


cursor.execute("SELECT COUNT(*) FROM employees")
print("COUNT emplyees =", cursor.fetchone()[0])

cursor.execute("SELECT MAX(id) FROM employees")
print("MAX id =", cursor.fetchone()[0])

cursor.execute("SELECT MIN(id) FROM employees")
print("MIN id =", cursor.fetchone()[0])

cursor.execute("SELECT SUM(id) FROM employees")
print("SUM id =", cursor.fetchone()[0])

cursor.execute("SELECT AVG(id) FROM employees")
print("AVG id =", cursor.fetchone()[0])

cursor.execute("SELECT COUNT(*) FROM job_titles")
print("COUNT job titles =", cursor.fetchone()[0])
print("\n")


cursor.execute("""
    SELECT jt.name, COUNT(e.id)
    FROM job_titles jt
    LEFT JOIN employees e ON jt.id_job_title = e.id_job_title
    GROUP BY jt.id_job_title
""")
for row in cursor.fetchall():
    print("Doljnost:", row[0], "| Kol-vo:", row[1])
print()

cursor.execute("""
    SELECT jt.name, AVG(e.id)
    FROM job_titles jt
    LEFT JOIN employees e ON jt.id_job_title = e.id_job_title
    GROUP BY jt.id_job_title
""")
for row in cursor.fetchall():
    print("Doljnost:", row[0], "| Srednii id:", row[1])
print()

cursor.execute("""
    SELECT jt.name, MAX(e.id), MIN(e.id)
    FROM job_titles jt
    LEFT JOIN employees e ON jt.id_job_title = e.id_job_title
    GROUP BY jt.id_job_title
""")
for row in cursor.fetchall():
    print("Doljnost:", row[0], "| Max id:", row[1], "| Min id:", row[2])
print()


cursor.execute("""
    SELECT e.surname, e.name, jt.name
    FROM employees e
    JOIN job_titles jt ON e.id_job_title = jt.id_job_title
""")
print("Spisok vseh:")
for row in cursor.fetchall():
    print(" -", row[0], row[1], "->", row[2])
print()

cursor.execute("""
    SELECT e.surname, e.name
    FROM employees e
    JOIN job_titles jt ON e.id_job_title = jt.id_job_title
    WHERE jt.name = 'Razrabotchik'
""")
print("Logo Razrabotchiki:")
for row in cursor.fetchall():
    print(" -", row[0], row[1])
print()

cursor.execute("""
    SELECT e.surname, e.name, jt.name
    FROM employees e
    JOIN job_titles jt ON e.id_job_title = jt.id_job_title
    WHERE e.surname LIKE 'S%'
""")
print("Familia na S:")
for row in cursor.fetchall():
    print(" -", row[0], row[1], "->", row[2])
print()

connection.close()