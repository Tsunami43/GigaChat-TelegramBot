from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext

from bot.filters import Admin
from bot import keyboards

from utils.session import Authorization
import data

router = Router()

class AppAccount(StatesGroup):
    account=State()
    api_id=State()
    api_hash=State()
    phone=State()
    code=State()
    password=State()
    void=State()

@router.message(Admin(), StateFilter(AppAccount), F.text=="❌ Отменить действие")
async def cancel_append_account(message: Message, state: FSMContext):
    user_data = await state.get_data()
    if user_data:
        await user_data['account'].cancel_authorization()
    await state.clear()
    await message.answer(
        text=
            "<b>Список комманд:</b>\n\n"+
            "▶️ Запустить - <i>запуск комментирования</i>\n\n"+
            "⏹ Остановить - <i>остановить комментирование</i>\n\n"+
            "➕ Добавить аккаунт - <i>добавить аккаунт</i>",
        parse_mode="HTML",
        reply_markup=keyboards.start()
    )

@router.message(Admin(), StateFilter(None), F.text=="➕ Добавить аккаунт")
async def app_account_handler(message: Message, state: FSMContext):
    await state.set_state(AppAccount.account)
    await message.answer(
        text=
            "Для добавления аккаунта необходимо предоставить следующие данные:\n\n"+
            "<b>* Название аккаунта</b> <i>( рекомендуем использовать <b>username</b> аккаунта)</i>\n\n"+
            "<b>* api id</b>\n\n"+
            "<b>* api hash</b>\n\n"+
            "<b>* Номер телефона</b> <i>(пример: +79876543210)</i>\n\n"+
            "<b>* Пароль</b> <i> (2fa если потребуется)</i>\n\n"+
            "Руководство по получению <b>api id/hash</b> приведенно по следующей ссылке "+
            "https://telegram-spam-master.com/telegram-api-id-and-hash.html",
        parse_mode="HTML",
        reply_markup=keyboards.cancel(),
        disable_web_page_preview=True
    )
    await message.answer(
        text=
            "Введите <b>название аккаунта</b>:",
        parse_mode="HTML"
    )

@router.message(AppAccount.account, F.text)
async def name_account_handler(message: Message, state: FSMContext):
    await state.set_state(AppAccount.api_id)
    await state.update_data(
        account=Authorization(
            message.text.strip()
        )
    )
    await message.answer(
        text=
            "Введите <b>api id</b>:",
        parse_mode="HTML"
    )

@router.message(AppAccount.api_id, F.text)
async def api_id_account_handler(message: Message, state: FSMContext):
    api_id = message.text.strip()
    if api_id.isdigit():
        await state.set_state(AppAccount.api_hash)
        user_data = await state.get_data()
        user_data['account'].api_id=int(api_id)
        await message.answer(
            text=
                "Введите <b>api hash</b>:",
            parse_mode="HTML"
        )
    else:
        await message.answer(
            text=
                "<b><i>Ошибка!</i></b>\n\n"+
                "Повторите ввод api id (обычно это целочисленное значение):",
            parse_mode="HTML"
        )

@router.message(AppAccount.api_hash, F.text)
async def api_hash_account_handler(message: Message, state: FSMContext):
    await state.set_state(AppAccount.phone)
    api_hash = message.text.strip()
    user_data = await state.get_data()
    user_data['account'].api_hash=api_hash
    await message.answer(
        text=
            "Введите <b>номер телефона</b> <i>(пример: +79876543210)</i>:",
        parse_mode="HTML"
    )


@router.message(AppAccount.phone, F.text)
async def phone_account_handler(message: Message, state: FSMContext):
    await state.set_state(AppAccount.void)
    await message.answer(
        text=
            "<b><i>Идет процесс аутентификации...</i></b>",
        parse_mode="HTML"
    )
    phone = message.text.strip()
    user_data = await state.get_data()
    account = user_data['account']
    account.phone=phone
    match (await account.send_code()):
        case (1):
            await state.set_state(AppAccount.code)
            await message.answer(
                text=
                    "<b><i>Аутентификация прошла успешно !</i></b>",
                parse_mode="HTML"
            )
            await message.answer(
                text=
                    "Введите <b>код</b> <i>(отправленный вам только что)</i>:",
                parse_mode="HTML"
            )
        case (10):
            await state.clear()
            await message.answer(
                text=
                    "<b><i>Ошибка!</i></b>\n\n"+
                    "Не правильно указан <b>api id/hash</b>.",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        case (11):
            await state.clear()
            await message.answer(
                text=
                    "<b><i>Ошибка!</i></b>\n\n"+
                    "Не правильно указан <b>номер телефона</b>.",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        case (12):
            await state.clear()
            await message.answer(
                text=
                    "<b><i>Ошибка!</i></b>\n\n"+
                    "Номер телефона <b>заблокирован</b>.",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        case (0):
            await state.clear()
            await message.answer(
                text=
                    "<b><i>Ошибка!</i></b>\n\n"+
                    "Не предвиденная ошибка - обратитесь к администратору.",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )

    

@router.message(AppAccount.code, F.text)
async def code_account_handler(message: Message, state: FSMContext):
    await state.set_state(AppAccount.void)
    await message.answer(
        text=
            "<b><i>Идет процесс авторизации...</i></b>",
        parse_mode="HTML"
    )
    code = message.text.strip()
    user_data = await state.get_data()
    account = user_data['account']
    account.phone_code=code
    match (await account.check_code()):
        case (1):
            await state.clear()
            await message.answer(
                text=
                    "<b><i>Авторизация прошла успешно !</i></b>\n\n"+
                    "Аккаунт добавлен.",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        case (10):
            await state.set_state(AppAccount.password)
            await message.answer(
                text=
                    "<i>Для входа требуется <b>2fa-пароль</b></i>\n\n"+
                    "Введите <b>пароль</b>:",
                parse_mode="HTML"
            )
        case (11):
            await state.clear()
            await message.answer(
                text=
                    "<b><i>Ошибка!</i></b>\n\n"+
                    "Код недействительный.",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        case (0):
            await state.clear()
            await message.answer(
                text=
                    "<b><i>Ошибка!</i></b>\n\n"+
                    "Не предвиденная ошибка - обратитесь к администратору.",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )

@router.message(AppAccount.password, F.text)
async def password_account_handler(message: Message, state: FSMContext):
    await state.set_state(AppAccount.void)
    await message.answer(
        text=
            "<b><i>Идет повторный процесс авторизации...</i></b>",
        parse_mode="HTML"
    )
    password = message.text.strip()
    user_data = await state.get_data()
    account = user_data['account']
    account.password=password
    match (await account.check_password()):
        case (1):
            await message.answer(
                text=
                    "<b><i>Авторизация прошла успешно !</i></b>\n\n"+
                    "Аккаунт добавлен.",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        case (10):        
            await message.answer(
                text=
                    "<b><i>Ошибка!</i></b>\n\n"+
                    "Не предвиденная ошибка - обратитесь к администратору.",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        case (0):
            await message.answer(
                text=
                    "<b><i>Ошибка!</i></b>\n\n"+
                    "Пароль неверен. Попробуйте снова.",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
    await state.clear()