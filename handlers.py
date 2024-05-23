import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext
from database import add_product, get_products, approve_product, edit_product, delete_product

logging.basicConfig(level=logging.INFO)

def start_handler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Добро пожаловать в бот-магазин!")

def create_product_handler(update: Update, context: CallbackContext):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Пожалуйста, предоставьте следующую информацию о новом продукте:")
    context.bot.send_message(chat_id=update.effective_chat.id, text="Название продукта:")
    name_handler = context.bot.register_next_step_handler(update.message, get_product_description)
    name_handler.user_data = {'user_id': update.effective_user.id}

def get_product_description(update: Update, context: CallbackContext):
    context.user_data['name'] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Описание продукта:")
    description_handler = context.bot.register_next_step_handler(update.message, get_product_price)
    description_handler.user_data = context.user_data

def get_product_price(update: Update, context: CallbackContext):
    context.user_data['description'] = update.message.text
    context.bot.send_message(chat_id=update.effective_chat.id, text="Цена продукта:")
    price_handler = context.bot.register_next_step_handler(update.message, save_product)
    price_handler.user_data = context.user_data

def save_product(update: Update, context: CallbackContext):
    try:
        price = float(update.message.text)
        user_id = context.user_data['user_id']
        name = context.user_data['name']
        description = context.user_data['description']
        add_product(name, description, price, user_id)
        context.bot.send_message(chat_id=update.effective_chat.id, text="Продукт успешно создан!")
    except ValueError:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Неверная цена. Пожалуйста, попробуйте снова.")

def admin_panel_handler(update: Update, context: CallbackContext):
    products = get_products()
    if not products:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Нет продуктов для одобрения.")
        return

    keyboard = []
    for product in products:
        keyboard.append([
            InlineKeyboardButton(f"Одобрить {product['name']}", callback_data=f"approve_{product['id']}"),
            InlineKeyboardButton(f"Редактировать {product['name']}", callback_data=f"edit_{product['id']}"),
            InlineKeyboardButton(f"Удалить {product['name']}", callback_data=f"delete_{product['id']}")
        ])

    reply_markup = InlineKeyboardMarkup(keyboard)
    context.bot.send_message(chat_id=update.effective_chat.id, text="Панель администратора:", reply_markup=reply_markup)

def user_panel_handler(update: Update, context: CallbackContext):
    products = get_products(approved=True)
    if not products:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Нет одобренных продуктов.")
        return

    keyboard = []
    for product in products:
        keyboard.append([InlineKeyboardButton(f"{product['name']} - {product['price']} руб.", callback_data=f"buy_{product['id']}")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.effective_chat.id, text="Панель пользователя:", reply_markup=reply_markup)

def approve_product_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    product_id = int(query.data.split('_')[1])
    approve_product(product_id)
    query.answer()
    query.edit_message_text(text=f"Продукт одобрен.")

def edit_product_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    product_id = int(query.data.split('_')[1])
    # Реализуйте логику редактирования продукта
    query.answer()
    query.edit_message_text(text=f"Продукт отредактирован.")

def delete_product_handler(update: Update, context: CallbackContext):
    query = update.callback_query
    product_id = int(query.data.split('_')[1])
    delete_product(product_id)
    query.answer()
    query.edit_message_text(text=f"Продукт удален.")
