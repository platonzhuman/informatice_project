import sqlite3
import csv

connection = sqlite3.connect('baza.db')
cursor = connection.cursor()

# CREATE TABLE
cursor.execute('''
CREATE TABLE store (
    store_id TEXT PRIMARY KEY,
    district TEXT,
    address TEXT
)
''')

cursor.execute('''
CREATE TABLE product (
    article INTEGER PRIMARY KEY,
    department TEXT,
    name TEXT,
    unit TEXT,
    quantity_per_pack REAL,
    supplier TEXT
)
''')

cursor.execute('''
CREATE TABLE movement (
    operation_id INTEGER PRIMARY KEY,
    date TEXT,
    store_id TEXT,
    article INTEGER,
    operation_type TEXT,
    packs INTEGER,
    price REAL,
    FOREIGN KEY (store_id) REFERENCES store(store_id),
    FOREIGN KEY (article) REFERENCES product(article)
)
''')

# MAGAZINE
with open('magazin.txt', 'r', encoding='utf-8-sig') as f:
    r = csv.reader(f, delimiter='\t')
    next(r) 
    for row in r:
        if not row:
            continue
        cursor.execute('INSERT INTO store (store_id, district, address) VALUES (?, ?, ?)',
                    (row[0].strip(), row[1].strip(), row[2].strip()))

# TOVAR
with open('tovar.txt', 'r', encoding='utf-8-sig') as f:
    r = csv.reader(f, delimiter='\t')
    next(r)
    for row in r:
        if not row:
            continue
        art = int(row[0].strip())
        depa = row[1].strip()
        name = row[2].strip()
        unit = row[3].strip()
        qty = row[4].strip().replace(',', '.')
        qu_pack = float(qty)
        supp = row[5].strip()
        cursor.execute('INSERT INTO product VALUES (?, ?, ?, ?, ?, ?)',
                    (art,
                      depa,
                        name,
                          unit,
                            qu_pack,
                              supp))


# DVIZ_TOVAR
with open('dviz_tovar.txt', 'r', encoding='utf-8-sig') as f:
    r = csv.reader(f, delimiter='\t')
    next(r)
    for row in r:
        if not row or len(row) < 7:
            continue
        id = int(row[0].strip())
        date = row[1].strip()
        store_id = row[2].strip()
        art = int(row[3].strip())
        pack = int(row[4].strip()) 
        optype = row[5].strip()        
        price = float(row[6].strip().replace(',', '.'))
        cursor.execute('''
            INSERT INTO movement (operation_id, date, store_id, article, operation_type, packs, price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (id, 
              date,
                store_id,
                  art,
                    optype,
                      pack,
                        price))

connection.commit()

query = '''
SELECT SUM(m.packs * p.quantity_per_pack) AS total_kg
FROM movement m
JOIN store s ON m.store_id = s.store_id
JOIN product p ON m.article = p.article
WHERE m.operation_type = 'Продажа'
  AND m.date BETWEEN '01.06.2021' AND '10.06.2021'
  AND s.district = 'Заречный'
  AND p.name = 'Паштет из куриной печени'
'''
result = cursor.execute(query).fetchone()[0]
print(f"Продано килограммов паштета из куриной печени: {result 
                                                        if result is not None 
                                                        else 0}")

connection.close()