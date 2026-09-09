import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler

# --- Import your animal data ---
from animals_data import ANIMALS, get_daily_content

# --- Setup ---
TOKEN = os.environ.get("BOT_TOKEN")
if not TOKEN:
    raise ValueError("No BOT_TOKEN found! Set it in Railway environment variables.")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Khmer Messages ---
WELCOME_TEXT = (
    "សួស្តី! សូមស្វាគមន៍មកកាន់ មេបក្សីធំ Bot 🐦\n\n"
    "ខ្ញុំអាចជួយអ្នកស្វែងយល់អំពីសត្វដែលអាចហើរ និងហែលទឹកបាន។\n"
    "សូមជ្រើសរើសមុខងារខាងក្រោម៖"
)

HELP_TEXT = (
    "របៀបប្រើប្រាស់៖\n"
    "/start - ចាប់ផ្តើមប្រើប្រាស់\n"
    "/daily - ទទួលបានព័ត៌មានប្រចាំថ្ងៃ\n"
    "/animals - បង្ហាញបញ្ជីសត្វ\n"
    "ឬចុចប៊ូតុងខាងក្រោម!"
)

# --- Command Handlers ---
def start(bot, update):
    keyboard = [
        [InlineKeyboardButton("ព័ត៌មានប្រចាំថ្ងៃ 📅", callback_data="daily")],
        [InlineKeyboardButton("បញ្ជីសត្វ 📋", callback_data="list_animals")],
        [InlineKeyboardButton("ជំនួយ ❓", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup)

def daily(bot, update):
    animal = get_daily_content()
    if animal:
        caption = f"**{animal['name_kh']}**\n\n{animal['description']}"
        if 'image_path' in animal and animal['image_path']:
            try:
                with open(animal['image_path'], 'rb') as photo:
                    update.message.reply_photo(photo=photo, caption=caption)
            except:
                update.message.reply_text(caption + "\n\n(រូបភាពមិនមាន)")
        else:
            update.message.reply_text(caption)
    else:
        update.message.reply_text("មិនមានព័ត៌មានសម្រាប់ថ្ងៃនេះទេ!")

def list_animals(bot, update):
    keyboard = []
    for key, animal in ANIMALS.items():
        keyboard.append([InlineKeyboardButton(animal['name_kh'], callback_data=f"animal_{key}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("សូមជ្រើសរើសសត្វដែលអ្នកចង់ដឹង៖", reply_markup=reply_markup)

def animal_detail(bot, update, animal_key):
    animal = ANIMALS.get(animal_key)
    if animal:
        caption = f"**{animal['name_kh']}**\n\n{animal['description']}"
        update.message.reply_text(caption)
    else:
        update.message.reply_text("រកមិនឃើញសត្វនេះទេ!")

def button_handler(bot, update):
    query = update.callback_query
    query.answer()
    
    data = query.data
    if data == "daily":
        daily(bot, query.message)
    elif data == "list_animals":
        list_animals(bot, query.message)
    elif data == "help":
        query.edit_message_text(HELP_TEXT)
    elif data.startswith("animal_"):
        animal_key = data.split("_", 1)[1]
        animal_detail(bot, query.message, animal_key)

def error_handler(bot, update, error):
    logger.error(f"Update {update} caused error {error}")

# --- Main Function ---
def main():
    # Create the Updater (without use_context for compatibility)
    updater = Updater(TOKEN)
    dp = updater.dispatcher
    
    # Register command handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("daily", daily))
    dp.add_handler(CommandHandler("animals", list_animals))
    dp.add_handler(CallbackQueryHandler(button_handler))
    dp.add_error_handler(error_handler)
    
    # Start the bot
    logger.info("Bot is starting...")
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
