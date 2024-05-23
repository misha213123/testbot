import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

def create_table():
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS products
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, description TEXT, price REAL, user_id INTEGER, approved BOOLEAN DEFAULT 0)''')
    conn.commit()
    conn.close()

create_table()

def add_product(name, description, price, user_id):
    logging.info(f"Adding product: name={name}, description={description}, price={price}, user_id={user_id}")
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("INSERT INTO products (name, description, price, user_id) VALUES (?, ?, ?, ?)", (name, description, price, user_id))
    conn.commit()
    conn.close()

def get_products(approved=False):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    if approved:
        c.execute("SELECT id, name, description, price, user_id FROM products WHERE approved = 1")
    else:
        c.execute("SELECT id, name, description, price, user_id FROM products")
    products = c.fetchall()
    conn.close()
    return [{'id': product[0], 'name': product[1], 'description': product[2], 'price': product[3], 'user_id': product[4]} for product in products]

def approve_product(product_id):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("UPDATE products SET approved = 1 WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()

def edit_product(product_id, name, description, price):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("UPDATE products SET name = ?, description = ?, price = ? WHERE id = ?", (name, description, price, product_id))
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = sqlite3.connect('products.db')
    c = conn.cursor()
    c.execute("DELETE FROM products WHERE id = ?", (product_id,))
    conn.commit()
    conn.close()
