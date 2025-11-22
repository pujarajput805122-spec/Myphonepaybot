import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_1 = int(os.getenv("CHANNEL_1", "0"))
CHANNEL_2 = int(os.getenv("CHANNEL_2", "0"))
CHANNEL_1_URL = os.getenv("CHANNEL_1_URL", "")
CHANNEL_2_URL = os.getenv("CHANNEL_2_URL", "")
APK_PATH = os.getenv("APK_PATH", "PhonePe_1.0.apk")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Join Channel 1", url=CHANNEL_1_URL),
            InlineKeyboardButton("Join Channel 2", url=CHANNEL_2_URL)
        ],
        [InlineKeyboardButton("Verify", callback_data="verify")]
    ]
    await update.message.reply_text(
        "🚀 Please join both channels to continue:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    try:
        status1 = await context.bot.get_chat_member(CHANNEL_1, user_id)
        status2 = await context.bot.get_chat_member(CHANNEL_2, user_id)
    except Exception as e:
        logger.error(f"Error checking channel membership: {e}")
        await query.answer("❌ Channels not found!", show_alert=True)
        return

    if status1.status in ["member", "administrator", "creator"] and \
       status2.status in ["member", "administrator", "creator"]:

        keyboard = [
            [InlineKeyboardButton("Get APK 🎁", callback_data="get_apk")]
        ]

        await query.message.edit_text(
            "✅ Verified! You can now download the APK:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    else:
        await query.answer("❌ Please join both channels first!", show_alert=True)

async def send_apk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    
    try:
        with open(APK_PATH, "rb") as apk_file:
            await query.message.reply_document(document=apk_file)
        await query.answer()
        logger.info(f"APK sent to user {query.from_user.id}")
    except FileNotFoundError:
        logger.error(f"APK file not found: {APK_PATH}")
        await query.answer("❌ APK not found!", show_alert=True)
    except Exception as e:
        logger.error(f"Error sending APK: {e}")
        await query.answer("❌ Error sending APK!", show_alert=True)

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable not set!")
        print("❌ Error: BOT_TOKEN environment variable is required.")
        print("Please set it in your environment variables.")
        return
    
    if not CHANNEL_1 or not CHANNEL_2:
        logger.error("Channel IDs not properly configured!")
        print("❌ Error: CHANNEL_1 and CHANNEL_2 environment variables are required.")
        return
    
    if not CHANNEL_1_URL or not CHANNEL_2_URL:
        logger.error("Channel URLs not properly configured!")
        print("❌ Error: CHANNEL_1_URL and CHANNEL_2_URL environment variables are required.")
        return

    logger.info("Starting bot...")
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(verify, pattern="verify"))
    app.add_handler(CallbackQueryHandler(send_apk, pattern="get_apk"))

    logger.info("Bot is running. Press Ctrl+C to stop.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
