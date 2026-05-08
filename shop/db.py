import sqlite3, os

DB = 'shop.db'

def init():
    if os.path.exists(DB):
        os.remove(DB)  # forclera start
    conn = sqlite3.connect(DB)
    cur = conn.cursor()

    cur.executescript('''
        CREATE TABLE producrs (
            id_product INTEGER PRIMARY KEY UNIQUE,
            name_of_product TEXT NOT NULL,
            price REAL NOT NULL,
            id_category INTEGER NOT NULL,
            quantity_at_storage REAL NOT NULL,
            FOREIGN KEY(id_category) REFERENCES categories(id_category)
        );
        CREATE TABLE categories (
            id_category INTEGER PRIMARY KEY UNIQUE,
            name_category TEXT NOT NULL
        );
        CREATE TABLE sale_items (
            id_sale INTEGER PRIMARY KEY UNIQUE,
            id_check INTEGER NOT NULL,
            id_product INTEGER NOT NULL,
            quantity REAL NOT NULL,
            FOREIGN KEY(id_check) REFERENCES reseipts(id_check),
            FOREIGN KEY(id_product) REFERENCES producrs(id_product)
        );
        CREATE TABLE reseipts (
            id_check INTEGER PRIMARY KEY UNIQUE,
            created_at REAL NOT NULL,
            id_cashier INTEGER NOT NULL,
            FOREIGN KEY(id_cashier) REFERENCES emploees(id)
        );
        CREATE TABLE emploees (
            id INTEGER PRIMARY KEY UNIQUE,
            name TEXT NOT NULL,
            surnaame TEXT NOT NULL,
            id_job_title INTEGER NOT NULL,
            FOREIGN KEY(id_job_title) REFERENCES jobs_titles(id)
        );
        CREATE TABLE jobs_titles (
            id INTEGER PRIMARY KEY UNIQUE,
            name TEXT NOT NULL
        );
    ''')
    
    # for worrk danue 
    cur.execute("INSERT INTO jobs_titles (name) VALUES ('кассир')")
    cur.execute("INSERT INTO emploees (name, surnaame, id_job_title) VALUES ('Иван', 'Петров', 1)")
    cur.executemany("INSERT INTO categories (name_category) VALUES (?)", [('Фрукты',), ('Молоко',)])
    cur.executemany('INSERT INTO producrs (name_of_product, price, id_category, quantity_at_storage) VALUES (?,?,?,?)', [
        ('Яблоки', 80, 1, 50), ('Бананы', 120, 1, 30), ('Молоко', 70, 2, 20)
    ])
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init()
    print("БД создана с вашими таблицами")