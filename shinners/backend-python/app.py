import sqlite3
import os
import json
import requests
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), '..', 'frontend')

app = Flask(__name__, static_folder=FRONTEND_DIR, static_url_path='')
CORS(app)

@app.route('/')
def serve_index():
    return send_from_directory(FRONTEND_DIR, 'index.html')

@app.route('/<path:path>')
def serve_frontend(path):
    file_path = os.path.join(FRONTEND_DIR, path)
    if os.path.exists(file_path) and not os.path.isdir(file_path):
        return send_from_directory(FRONTEND_DIR, path)
    return send_from_directory(FRONTEND_DIR, 'index.html')

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'database', 'shinners.db')
JAVA_SERVICE_URL = "http://localhost:8081"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    schema_path = os.path.join(os.path.dirname(__file__), '..', 'database', 'schema.sql')
    conn.executescript(open(schema_path).read())
    conn.commit()
    conn.close()

init_db()

@app.route('/api/products', methods=['GET'])
def get_products():
    conn = get_db()
    category = request.args.get('category')
    search = request.args.get('search')
    query = "SELECT * FROM products"
    params = []
    conditions = []
    if category:
        conditions.append("category = ?")
        params.append(category)
    if search:
        conditions.append("(name LIKE ? OR description LIKE ?)")
        params.append(f"%{search}%")
        params.append(f"%{search}%")
    if conditions:
        query += " WHERE " + " AND ".join(conditions)
    query += " ORDER BY id DESC"
    rows = conn.execute(query, params).fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM products WHERE id = ?", (product_id,)).fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({"error": "Product not found"}), 404

@app.route('/api/categories', methods=['GET'])
def get_categories():
    conn = get_db()
    rows = conn.execute("SELECT DISTINCT category FROM products ORDER BY category").fetchall()
    conn.close()
    return jsonify([r["category"] for r in rows])

@app.route('/api/cart', methods=['GET', 'POST', 'DELETE'])
def cart_handler():
    session_id = request.args.get('session_id', 'default')
    try:
        if request.method == 'GET':
            resp = requests.get(f"{JAVA_SERVICE_URL}/cart?session_id={session_id}", timeout=2)
            return jsonify(resp.json())
        elif request.method == 'POST':
            data = request.get_json()
            resp = requests.post(f"{JAVA_SERVICE_URL}/cart?session_id={session_id}",
                                 json=data, timeout=2)
            return jsonify(resp.json())
        elif request.method == 'DELETE':
            resp = requests.delete(f"{JAVA_SERVICE_URL}/cart?session_id={session_id}", timeout=2)
            return jsonify(resp.json())
    except requests.exceptions.ConnectionError:
        return jsonify({"error": "Cart service unavailable", "items": [], "total": 0, "tax": 0, "grand_total": 0}), 503

@app.route('/api/orders', methods=['POST'])
def place_order():
    data = request.get_json()
    conn = get_db()
    try:
        cur = conn.execute(
            "INSERT INTO orders (customer_name, customer_email, customer_address, total, tax, discount) VALUES (?, ?, ?, ?, ?, ?)",
            (data['name'], data['email'], data['address'], data['total'], data['tax'], data.get('discount', 0))
        )
        order_id = cur.lastrowid
        for item in data['items']:
            conn.execute(
                "INSERT INTO order_items (order_id, product_id, product_name, quantity, price, size, color) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (order_id, item['id'], item['name'], item['quantity'], item['price'], item.get('size', ''), item.get('color', ''))
            )
        conn.commit()
        return jsonify({"success": True, "order_id": order_id}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

@app.route('/api/orders', methods=['GET'])
def get_orders():
    conn = get_db()
    rows = conn.execute("SELECT * FROM orders ORDER BY created_at DESC").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/books', methods=['GET'])
def get_books():
    conn = get_db()
    rows = conn.execute("SELECT * FROM books ORDER BY id").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

@app.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    conn = get_db()
    row = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()
    if row:
        return jsonify(dict(row))
    return jsonify({"error": "Book not found"}), 404

@app.route('/api/books', methods=['POST'])
def add_book():
    data = request.get_json()
    conn = get_db()
    cur = conn.execute(
        "INSERT INTO books (title, author, price, image_url) VALUES (?, ?, ?, ?)",
        (data['title'], data['author'], data.get('price', 14.99), data.get('image_url', ''))
    )
    conn.commit()
    book_id = cur.lastrowid
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()
    return jsonify(dict(book)), 201

@app.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    data = request.get_json()
    conn = get_db()
    conn.execute(
        "UPDATE books SET title = ?, author = ?, price = ? WHERE id = ?",
        (data['title'], data['author'], data.get('price', 14.99), book_id)
    )
    conn.commit()
    book = conn.execute("SELECT * FROM books WHERE id = ?", (book_id,)).fetchone()
    conn.close()
    if book:
        return jsonify(dict(book))
    return jsonify({"error": "Book not found"}), 404

@app.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    conn = get_db()
    conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
    conn.commit()
    conn.close()
    return jsonify({"success": True, "message": "Book deleted"})

@app.route('/api/sizes', methods=['GET'])
def get_sizes():
    conn = get_db()
    # Return distinct sizes from all products
    rows = conn.execute("SELECT sizes FROM products").fetchall()
    conn.close()
    all_sizes = set()
    for r in rows:
        for s in r["sizes"].split(","):
            all_sizes.add(s.strip())
    return jsonify(sorted(all_sizes))

if __name__ == '__main__':
    from seed import seed
    if not os.path.exists(DB_PATH):
        seed()
    print("Starting Python backend on http://localhost:5000")
    app.run(debug=True, port=5000)
