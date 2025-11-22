import logging
import os
import time
from threading import Thread
from flask import Flask
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from telegram.request import HTTPXRequest

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()

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

COOLDOWN = {}
FILE_ID_CACHE = None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
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
        logger.info(f"Start message sent to user {update.message.from_user.id}")
    except Exception as e:
        logger.error(f"Error in start: {e}")

async def verify(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    
    try:
        # Acknowledge the button click
        await query.answer()
        
        if user_id in COOLDOWN and COOLDOWN[user_id] > time.time():
            await query.answer("⏳ Slow down! Try again in 3 seconds.", show_alert=True)
            return
        COOLDOWN[user_id] = time.time() + 3
        
        status1 = await context.bot.get_chat_member(CHANNEL_1, user_id)
        status2 = await context.bot.get_chat_member(CHANNEL_2, user_id)
        
        if status1.status in ["member", "administrator", "creator"] and \
           status2.status in ["member", "administrator", "creator"]:
            keyboard = [
                [InlineKeyboardButton("Get APK 🎁", callback_data="get_apk")]
            ]
            await query.edit_message_text(
                text="✅ Verified! You can now download the APK:",
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
            logger.info(f"User {user_id} verified successfully")
        else:
            await query.answer("❌ Please join both channels first!", show_alert=True)
            logger.info(f"User {user_id} not a member of both channels")
    except Exception as e:
        logger.error(f"Error in verify: {e}")
        try:
            await query.answer(f"❌ Error: {str(e)[:50]}", show_alert=True)
        except:
            pass

async def send_apk(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global FILE_ID_CACHE
    query = update.callback_query
    user_id = query.from_user.id
    chat_id = query.message.chat_id
    
    try:
        await query.answer()
        
        if FILE_ID_CACHE:
            try:
                await context.bot.send_document(
                    chat_id=chat_id,
                    document=FILE_ID_CACHE,
                    caption="🔐 Password - tritalks",
                    protect_content=True
                )
                logger.info(f"APK sent to user {user_id} (cached)")
                return
            except Exception as e:
                logger.error(f"Error sending cached APK: {e}")
        
        with open(APK_PATH, "rb") as apk_file:
            msg = await context.bot.send_document(
                chat_id=chat_id,
                document=apk_file,
                caption="🔐 Password - tritalks",
                protect_content=True
            )
            if msg.document:
                FILE_ID_CACHE = msg.document.file_id
            logger.info(f"APK sent to user {user_id} (new)")
    except FileNotFoundError:
        logger.error(f"APK file not found: {APK_PATH}")
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text="❌ APK file not available. Please contact support."
            )
        except Exception as e:
            logger.error(f"Error sending file not found message: {e}")
    except Exception as e:
        logger.error(f"Error sending APK: {e}")
        try:
            await context.bot.send_message(
                chat_id=chat_id,
                text=f"❌ Error: {str(e)[:100]}"
            )
        except:
            pass

def main():
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN environment variable not set!")
        print("❌ Error: BOT_TOKEN environment variable is required.")
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
    keep_alive()
    
    request = HTTPXRequest(
        connection_pool_size=8,
        read_timeout=60.0,
        write_timeout=60.0,
        connect_timeout=10.0
    )
    bot_app = Application.builder().token(BOT_TOKEN).request(request).concurrent_updates(True).build()

    bot_app.add_handler(CommandHandler("start", start))
    bot_app.add_handler(CallbackQueryHandler(verify, pattern="verify"))
    bot_app.add_handler(CallbackQueryHandler(send_apk, pattern="get_apk"))

    logger.info("🤖 Bot is running 24/7!")
    bot_app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
