import os
import logging
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- Import your animal data ---
# You'll create this file in the next step
from animals_data import ANIMALS, get_daily_content

# --- Setup ---
TOKEN = os.environ.get("BOT_TOKEN") # Railway will set this
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
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("ព័ត៌មានប្រចាំថ្ងៃ 📅", callback_data="daily")],
        [InlineKeyboardButton("បញ្ជីសត្វ 📋", callback_data="list_animals")],
        [InlineKeyboardButton("ជំនួយ ❓", callback_data="help")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(WELCOME_TEXT, reply_markup=reply_markup)

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Get today's content (you can define logic in animals_data.py)
    animal = get_daily_content()
    if animal:
        caption = f"**{animal['name_kh']}**\n\n{animal['description']}"
        # Check if image path exists, else send text only
        if 'image_path' in animal and animal['image_path']:
             # For Railway, you'd need to serve images via a static folder or URL
             # This example assumes you have the image file in a 'static' folder
             with open(animal['image_path'], 'rb') as photo:
                 await update.message.reply_photo(photo=photo, caption=caption)
        else:
             await update.message.reply_text(caption)
    else:
        await update.message.reply_text("មិនមានព័ត៌មានសម្រាប់ថ្ងៃនេះទេ!")

async def list_animals(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Send a list of animals with inline buttons
    keyboard = []
    for key, animal in ANIMALS.items():
        keyboard.append([InlineKeyboardButton(animal['name_kh'], callback_data=f"animal_{key}")])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("សូមជ្រើសរើសសត្វដែលអ្នកចង់ដឹង៖", reply_markup=reply_markup)

async def animal_detail(update: Update, context: ContextTypes.DEFAULT_TYPE, animal_key: str):
    animal = ANIMALS.get(animal_key)
    if animal:
        caption = f"**{animal['name_kh']}**\n\n{animal['description']}"
        # Same image logic as above
        await update.message.reply_text(caption)
    else:
        await update.message.reply_text("រកមិនឃើញសត្វនេះទេ!")

# --- Callback Query Handler ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer() # Acknowledge the button press

    data = query.data
    if data == "daily":
        await daily(update, context)
    elif data == "list_animals":
        await list_animals(update, context)
    elif data == "help":
        await query.edit_message_text(HELP_TEXT)
    elif data.startswith("animal_"):
        animal_key = data.split("_", 1)[1]
        await animal_detail(update, context, animal_key)

# --- Main Function ---
def main():
    app = Application.builder().token(TOKEN).build()

    # Register command handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("daily", daily))
    app.add_handler(CommandHandler("animals", list_animals))
    app.add_handler(CallbackQueryHandler(button_handler))

    # Start the bot
    logger.info("Bot is starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
