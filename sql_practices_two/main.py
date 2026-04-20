import sqlite3
import pandas as pd

conn = sqlite3.connect('uni.db')
cursor = conn.cursor()

cursor.executescript('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    fio TEXT,
    major TEXT,
    study_form TEXT,
    level TEXT,
    avg_score REAL
);
''')

try:
    df = pd.read_csv('students.csv')
    df.to_sql('students', conn, if_exists='append', index=False)
except:
    conn.commit()

queries = {
    "всего студентов": "SELECT COUNT(*) FROM students",
    "по направлениям": "SELECT major, COUNT(*) FROM students GROUP BY major",
    "по формам обучения": "SELECT study_form, COUNT(*) FROM students GROUP BY study_form",
    "мин/макс/средний балл по направлениям": "SELECT major, MAX(avg_score), MIN(avg_score), AVG(avg_score) FROM students GROUP BY major",
    "средний балл (направление + уровень + форма)": "SELECT major, level, study_form, AVG(avg_score) FROM students GROUP BY major, level, study_form",
    "топ-5 на стипендию (прикладная информатика, очно)": "SELECT fio, avg_score FROM students WHERE major = 'Прикладная Информатика' AND study_form = 'очная' ORDER BY avg_score DESC LIMIT 5",
    "количесто однофамилцев": "SELECT COUNT(*) FROM students WHERE fio IN (SELECT fio FROM students GROUP BY SUBSTR(fio, 1, INSTR(fio, ' ') - 1) HAVING COUNT(*) > 1)",
    "полные тэзки": "SELECT fio, COUNT(*) FROM students GROUP BY fio HAVING COUNT(*) > 1"
}

for desc, q in queries.items():
    print(f"\n{desc}")
    cursor.execute(q)
    for row in cursor.fetchall():
        print(row)

conn.close()
