import sqlite3

conn = sqlite3.connect('bs.db')
c = conn.cursor()

c.executescript('''
CREATE TABLE IF NOT EXISTS `уровни` (
    `id_ровня` integer primary key NOT NULL UNIQUE,
    `название` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `направления` (
    `id_направления` integer primary key NOT NULL UNIQUE,
    `название` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `типы` (
    `id_типа` integer primary key NOT NULL UNIQUE,
    `название` TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS `студенты` (
    `id_студента` integer primary key NOT NULL UNIQUE,
    `id_уровня` INTEGER NOT NULL,
    `id_направления` INTEGER NOT NULL,
    `id_типа` INTEGER NOT NULL,
    `фамилия` TEXT NOT NULL,
    `имя` TEXT NOT NULL,
    `средний_балл` REAL NOT NULL,
    FOREIGN KEY(`id_уровня`) REFERENCES `уровни`(`id_ровня`),
    FOREIGN KEY(`id_направления`) REFERENCES `направления`(`id_направления`),
    FOREIGN KEY(`id_типа`) REFERENCES `типы`(`id_типа`)
);
''')

c.executemany("INSERT OR IGNORE INTO `уровни` VALUES (?,?)", [(1,'бакалавриат'),(2,'магистратура'),(3,'аспирантура')])
c.executemany("INSERT OR IGNORE INTO `направления` VALUES (?,?)", [(1,'Информатика'),(2,'Математика'),(3,'Физика')])
c.executemany("INSERT OR IGNORE INTO `типы` VALUES (?,?)", [(1,'очное'),(2,'заочное'),(3,'вечернее')])

students_data = [
    (1, 1, 1, 1, 'Жуман', 'Платон', 4.8),
    (2, 1, 1, 1, 'Пермяков', 'Никита', 4.2),
    (3, 1, 2, 2, '', 'Максон', 3.8),
    (4, 2, 1, 1, '', 'антоха', 4.5),
    (5, 2, 3, 1, '', 'Даня', 3.9)
]

c.executemany("INSERT OR IGNORE INTO `студенты` VALUES (?,?,?,?,?,?,?)", students_data)
conn.commit()

print("\n--- Запросы с CASE ---")
for r in c.execute("SELECT `фамилия`, `имя`, `средний_балл`, CASE WHEN `средний_балл`>=4.5 THEN 'отлично' WHEN `средний_балл`>=3.5 THEN 'хорошо' ELSE 'удовл' END FROM `студенты`"):
    print(f"{r[0]} {r[1]}: {r[2]} - {r[3]}")

print("\n--- Запросы с ПОДЗАПРОСАМИ (выше среднего) ---")
for r in c.execute("SELECT `имя`, `средний_балл` FROM `студенты` WHERE `средний_балл` > (SELECT AVG(`средний_балл`) FROM `студенты`)"):
    print(f"{r[0]}: {r[1]}")

print("\n--- Запросы с CTE (инфо по направлению) ---")
query_cte = '''
WITH student_info AS (
    SELECT s.имя, s.средний_балл, n.название as напр
    FROM студенты s
    JOIN направления n ON s.id_направления = n.id_направления
)
SELECT * FROM student_info WHERE средний_балл > 4.0
'''
for r in c.execute(query_cte):
    print(f"{r[0]} ({r[2]}): {r[1]}")

conn.close()
print("\nДанные обновлены!")
