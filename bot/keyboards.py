from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder


def start()-> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    
    builder.row(
        KeyboardButton(text="▶️ Запустить"),
        KeyboardButton(text="⏹ Остановить")
    )

    builder.row(
        KeyboardButton(text="➕ Добавить аккаунт"),
        KeyboardButton(text="💬 Промт")
    )
    builder.row(
        KeyboardButton(text="⚙️ Параметры комментирования")
    )
    return builder.as_markup(resize_keyboard=True)


def cancel()-> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.button(text="❌ Отменить действие")
    return builder.as_markup(resize_keyboard=True)


def setting_sleep():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Изменить (от)",
        callback_data="sleep_start")
    )
    builder.add(InlineKeyboardButton(
        text="Изменить (до)",
        callback_data="sleep_end")
    )
    return builder.as_markup()


def setting_skip_msg():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Изменить (от)",
        callback_data="skip_msg_start")
    )
    builder.add(InlineKeyboardButton(
        text="Изменить (до)",
        callback_data="skip_msg_end")
    )
    return builder.as_markup()


def setting_skip_post():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Изменить (от)",
        callback_data="skip_post_start")
    )
    builder.add(InlineKeyboardButton(
        text="Изменить (до)",
        callback_data="skip_post_end")
    )
    return builder.as_markup()


def setting_skip_timeframe():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Изменить (от)",
        callback_data="skip_timeframe_start")
    )
    builder.add(InlineKeyboardButton(
        text="Изменить (до)",
        callback_data="skip_timeframe_end")
    )
    return builder.as_markup()


def setting_work_time():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Изменить (с)",
        callback_data="work_time_start")
    )
    builder.add(InlineKeyboardButton(
        text="Изменить (до)",
        callback_data="work_time_end")
    )
    return builder.as_markup()


def setting_emodji():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(
        text="Изменить (Да\Нет)",
        callback_data="emodji")
    )
    return builder.as_markup()