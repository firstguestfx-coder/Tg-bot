import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
)
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("8543772090:AAGQl7zhDbZAdlXl-uy2Z_5NwqTbwA5qLnQ")

# ✅ Yaha apne channels ke username daale (without @)
REQUIRED_CHANNELS = [
    "https://t.me/pcpanelsetup",
    "https://t.me/+e4q9PY6JG8QxOTM1",
    "https://t.me/+7MPeh5PUDZI1NjRl",
]

# /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []

    # Channel Join Buttons
    for channel in REQUIRED_CHANNELS:
        keyboard.append(
            [InlineKeyboardButton(f"Join {channel}", url=f"https://t.me/{channel}")]
        )

    # Check Joined Button
    keyboard.append(
        [InlineKeyboardButton("✅ Check Joined", callback_data="check_joined")]
    )

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "👋 Welcome!\n\n"
        "🔔 Please join all channels first.\n"
        "Then click ✅ Check Joined.",
        reply_markup=reply_markup,
    )


# Check Joined Button Logic
async def check_joined(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    not_joined = []

    for channel in REQUIRED_CHANNELS:
        try:
            member = await context.bot.get_chat_member(
                chat_id=f"@{channel}", user_id=user_id
            )

            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(channel)

        except:
            not_joined.append(channel)

    if not_joined:
        await query.edit_message_text(
            "❌ You have not joined all channels.\n\n"
            "Please join all channels and try again."
        )
    else:
        await query.edit_message_text(
            "🎉 Verified Successfully!\n\n"
            "You have joined all required channels."
        )


# Callback handler
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query

    if query.data == "check_joined":
        await check_joined(update, context)


# Main Function
def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()