import os
import logging
import sqlite3

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Подключение к базе данных
def connect_to_db():
    try:
        conn = sqlite3.connect(os.getenv('DB_FILE', 'products.db'))
        return conn
    except sqlite3.Error as e:
        logging.error(f"Ошибка при подключении к базе данных: {e}")
        return None

# Добавление продукта в базу данных
def add_product(name, description, price):
    conn = connect_to_db()
    if conn:
        try:
            c = conn.cursor()
            c.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)", (name, description, price))
            conn.commit()
            logging.info(f"Продукт '{name}' успешно добавлен.")
        except sqlite3.Error as e:
            logging.error(f"Ошибка при добавлении продукта: {e}")
        finally:
            conn.close()

# Получение списка всех продуктов
def get_all_products():
    conn = connect_to_db()
    if conn:
        try:
            c = conn.cursor()
            c.execute("SELECT * FROM products")
            products = c.fetchall()
            return products
        except sqlite3.Error as e:
            logging.error(f"Ошибка при получении списка продуктов: {e}")
            return None
        finally:
            conn.close()
