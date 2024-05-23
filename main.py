import os
import sqlite3
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Состояния для конверсационного режима
NAME, DESCRIPTION, PRICE = range(3)

# Подключение к базе данных
db_path = os.path.join(os.path.dirname(__file__), 'products.db')
conn = sqlite3.connect(db_path)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS products
             (name TEXT, description TEXT, price REAL)''')
conn.commit()
logging.info(f"Подключено к базе данных: {db_path}")

def add_product(name, description, price):
    try:
        c.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)", (name, description, price))
        conn.commit()
        logging.info(f"Добавлен продукт: {name}, {description}, {price}")
    except sqlite3.Error as e:
        logging.error(f"Ошибка при добавлении продукта: {e}")

def get_all_products():
    try:
        c.execute("SELECT name, description, price FROM products")
        return c.fetchall()
    except sqlite3.Error as e:
        logging.error(f"Ошибка при получении списка продуктов: {e}")
        return []

def handle_list_command(update, context):
    products = get_all_products()
    if not products:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Список продуктов пуст.")
    else:
        message = "Список всех продуктов:\n\n"
        for product in products:
            message += f"Название: {product[0]}\nОписание: {product[1]}\nЦена: {product[2]} руб.\n\n"
        context.bot.send_message(chat_id=update.effective_chat.id, text=message)

def handle_start_command(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Я бот для управления продуктами. Давайте добавим новый продукт. Напишите название продукта.")
    return NAME

def handle_name(update, context):
    context.user_data['name'] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Отлично, теперь напишите описание продукта.")
    return DESCRIPTION

def handle_description(update, context):
    context.user_data['description'] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Последний шаг, напишите цену продукта.")
    return PRICE

def handle_price(update, context):
    try:
        price = float(update.message.text)
        add_product(context.user_data['name'], context.user_data['description'], price)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Продукт успешно добавлен!")
        return ConversationHandler.END
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Неверный формат цены. Пожалуйста, введите число.")
        return PRICE
    except sqlite3.Error as e:
        logging.error(f"Ошибка при добавлении продукта: {e}")
        context.bot.send_message(chat_id=update.effective_chat.id, text="Произошла ошибка при добавлении продукта. Пожалуйста, попробуйте еще раз.")
        return ConversationHandler.END

def handle_cancel(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Операция отменена.")
    return ConversationHandler.END

def main():
    updater = Updater(token="6318762434:AAHzx_CIYs0Lmuj2H-Aj_wCrAeqMb8t3ktU", use_context=True)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("add", handle_start_command)],
        states={

            NAME: [MessageHandler(Filters.text & ~Filters.command, handle_name)],
            DESCRIPTION: [MessageHandler(Filters.text & ~Filters.command, handle_description)],
            PRICE: [MessageHandler(Filters.text & ~Filters.command, handle_price)]
        },
        fallbacks=[CommandHandler("cancel", handle_cancel)]
    )

    dispatcher.add_handler(conv_handler)
    dispatcher.add_handler(CommandHandler("list", handle_list_command))

    updater.start_polling()
    logging.info("Бот запущен.")
    updater.idle()

    # Закрытие соединения с базой данных
    conn.close()
    logging.info("Соединение с базой данных закрыто.")

if __name__ == '__main__':
    main()
