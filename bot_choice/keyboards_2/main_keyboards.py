from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


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
