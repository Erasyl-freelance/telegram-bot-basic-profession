from telebot.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from telebot import TeleBot

bot = TeleBot('7764736837:AAGbi64QSFH1bptdSnpfjsx5mx-p581UGTw')
user_choice = {}


def choose_profession_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("👨‍🔬 Scientist", callback_data="prof_scientist"),
        InlineKeyboardButton("🎵 Musician", callback_data="prof_musician"),
        InlineKeyboardButton("👩‍🚀 Cosmonaut", callback_data="prof_cosmonaut")
    )
    return kb


def ready_for_adventure_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("✅ Yes, I'm ready.", callback_data="adventure_yes"),
        InlineKeyboardButton("🤔 I'll think.", callback_data="adventure_no")
    )
    kb.add(
        InlineKeyboardButton("🔄 Start Over", callback_data="restart")
    )
    return kb


def restart_keyboard():
    kb = InlineKeyboardMarkup()
    kb.add(
        InlineKeyboardButton("🔄 Start Over", callback_data="restart")
    )
    return kb


@bot.message_handler(commands=["start"])
def hello_friends(message: Message):
    user_choice.pop(message.from_user.id, None)
    bot.send_message(
        message.from_user.id,
        "<b>Hey, friend! 👋</b>\nWhat do you want to become when you grow up?\n\n<em>Choose a profession below:</em>",
        parse_mode="HTML",
        reply_markup=choose_profession_keyboard()
    )


@bot.message_handler(commands=["help"])
def help_message(message: Message):
    bot.send_message(
        message.chat.id,
        "<b>ℹ️ How this bot works:</b>\n"
        "1️⃣ <b>Choose your dream profession</b> using the buttons.\n"
        "2️⃣ <b>Decide if you're ready</b> for an adventure.\n"
        "3️⃣ Use <b>🔄 Start Over</b> any time to begin again!\n"
        "<em>Repeat choices as much as you want 😉</em>",
        parse_mode="HTML",
        reply_markup=restart_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data == "restart")
def restart(call: CallbackQuery):
    user_choice.pop(call.from_user.id, None)
    try:
        bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    except Exception:
        pass
    bot.send_message(
        call.from_user.id,
        "<b>Let's start again! 👋</b>\nWhat do you want to become when you grow up?",
        parse_mode="HTML",
        reply_markup=choose_profession_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("prof_"))
def handle_profession(call: CallbackQuery):
    chosen = call.data
    prev_choice = user_choice.get(call.from_user.id)
    prof_map = {
        'prof_scientist': '👨‍🔬 <b>Scientist</b>',
        'prof_musician': '🎵 <b>Musician</b>',
        'prof_cosmonaut': '👩‍🚀 <b>Cosmonaut</b>'
    }
    if prev_choice == chosen:
        bot.answer_callback_query(call.id, "You've already chosen this profession! 😊", show_alert=False)
        bot.send_message(call.from_user.id,
                         "<em>You have already chosen this profession. Please select something else or continue.</em>",
                         parse_mode="HTML", reply_markup=restart_keyboard())
        return
    user_choice[call.from_user.id] = chosen
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    bot.send_message(
        call.from_user.id,
        f"Cool! You chose {prof_map.get(chosen, 'someone amazing. 🚀')}\n"
        f"<em>Are you ready for an adventure?</em>",
        parse_mode="HTML",
        reply_markup=ready_for_adventure_keyboard()
    )


@bot.callback_query_handler(func=lambda call: call.data.startswith("adventure_"))
def handle_adventure(call: CallbackQuery):
    bot.edit_message_reply_markup(call.from_user.id, call.message.message_id)
    if call.data == "adventure_yes":
        bot.send_message(
            call.from_user.id,
            "<b>Inspiration and adventures are waiting for you ahead! 🦸‍♂️</b>",
            parse_mode="HTML",
            reply_markup=restart_keyboard()
        )
    else:
        bot.send_message(
            call.from_user.id,
            "<em>When you're ready, let me know! 😉</em>",
            parse_mode="HTML",
            reply_markup=restart_keyboard()
        )


if __name__ == "__main__":
    bot.infinity_polling()
