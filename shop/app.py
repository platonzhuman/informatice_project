from flask import Flask, request, jsonify, render_template_string 
from datetime import datetime
import sqlite3, db

app = Flask(__name__)
db.init()

# for zapros
def query(sql, params=(), one=False):
    with sqlite3.connect('shop.db') as conn:
        res = conn.execute(sql, params).fetchall()
        return (res[0] if res else None) if one else res

with open('index.html', 'r', encoding='utf-8') as f:
    HTML = f.read()

@app.route('/')
def index():
    return render_template_string(HTML)

@app.route('/style.css')
def serve_css():
    with open('style.css', 'r') as f:
        return f.read(), 200, {'Content-Type': 'text/css'}

@app.route('/index.js')
def serve_js():
    with open('index.js', 'r') as f:
        return f.read(), 200, {'Content-Type': 'application/javascript'}

# list tovat
@app.route('/products')
def products():
    data = query('SELECT id_product, name_of_product, price, quantity_at_storage FROM producrs WHERE quantity_at_storage > 0')
    return jsonify([{'id': r[0], 'name': r[1], 'price': r[2], 'stock': r[3]} for r in data])

# for bye
@app.route('/sale', methods=['POST'])
def sale():
    req = request.json
    cashier, items = req['cashier_id'], req['items']
    
    with sqlite3.connect('shop.db') as conn:
        cur = conn.cursor()
        try:
            for i in items:
                stock = cur.execute('SELECT quantity_at_storage FROM producrs WHERE id_product = ?', (i['id_product'],)).fetchone()[0]
                if stock < i['quantity']:
                    return jsonify({'error': f'Товара {i["id_product"]} мало: {stock}'}), 400

            now = datetime.now().timestamp()
            cur.execute('INSERT INTO reseipts (created_at, id_cashier) VALUES (?, ?)', (now, cashier))
            bill_id = cur.lastrowid

            for i in items:
                cur.execute('INSERT INTO sale_items (id_check, id_product, quantity) VALUES (?, ?, ?)', (bill_id, i['id_product'], i['quantity']))
                cur.execute('UPDATE producrs SET quantity_at_storage = quantity_at_storage - ? WHERE id_product = ?', (i['quantity'], i['id_product']))
            
            conn.commit()
            return jsonify({'check_id': bill_id})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

# otchet
@app.route('/report')
def report():
    dt = request.args.get('date') 
    start = datetime.strptime(dt, '%Y-%m-%d').timestamp()
    end = start + 86399 

    item= query('''
        SELECT p.name_of_product, SUM(s.quantity), SUM(s.quantity * p.price)
        FROM sale_items s 
        JOIN producrs p ON s.id_product = p.id_product
        JOIN reseipts r ON s.id_check = r.id_check
        WHERE r.created_at BETWEEN ? AND ? GROUP BY p.id_product
    ''', (start, end))

    total = sum(row[2] for row in item)
    return jsonify({
        'date': dt, 
        'items': [{'name': r[0], 'qty': r[1]} for r in item], 
        'revenue': total
    })

if __name__ == '__main__':
    app.run(debug=True)
