from telegram.ext import Updater, CommandHandler, CallbackQueryHandler
from handlers import (
    start_handler, create_product_handler, admin_panel_handler,
    user_panel_handler, approve_product_handler, edit_product_handler,
    delete_product_handler
)

def main():
    updater = Updater(token='6318762434:AAHzx_CIYs0Lmuj2H-Aj_wCrAeqMb8t3ktU', use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_handler))
    dispatcher.add_handler(CommandHandler('create_product', create_product_handler))
    dispatcher.add_handler(CommandHandler('admin_panel', admin_panel_handler))
    dispatcher.add_handler(CommandHandler('user_panel', user_panel_handler))

    dispatcher.add_handler(CallbackQueryHandler(approve_product_handler, pattern='^approve_'))
    dispatcher.add_handler(CallbackQueryHandler(edit_product_handler, pattern='^edit_'))
    dispatcher.add_handler(CallbackQueryHandler(delete_product_handler, pattern='^delete_'))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
