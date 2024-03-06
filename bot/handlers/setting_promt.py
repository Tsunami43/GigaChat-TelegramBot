from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext

from bot.filters import Admin
from bot import keyboards

import data

router = Router()

class Promt(StatesGroup):
    promt=State()


@router.message(Admin(), StateFilter(Promt), F.text=="❌ Отменить действие")
async def cancel_promt(message: Message, state: FSMContext):
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

@router.message(Admin(), StateFilter(None), F.text=="💬 Промт")
async def promt_handler(message: Message, state: FSMContext):
    await state.set_state(Promt.promt)
    promt = data.read_setting()["Promt"]
    await message.answer(
        "<b>Действующий промт для комментирования:</b>\n\n"+
        f"<i><b>User:</b></i> {promt}\n\n"+
        "<i><b>GigaChat:</b></i> Понятно. Начнём?\n\n"+
        "<i><b>User:</b></i> ...\n\n"+
        "<i>Для изменения пришлите новый промт !</i>",
        parse_mode="HTML",
        reply_markup=keyboards.cancel()
    )

@router.message(Promt.promt, F.text)
async def promt_new(message: Message, state: FSMContext):
    try:
        data.write_promt(message.text)
        await message.answer(
            text=
                "<b>Промт изменен успешно !</b>",
            parse_mode="HTML",
            reply_markup=keyboards.start()
        )
    except:
        await message.answer(
            text=
                "<b>Ошибка !</b>",
            parse_mode="HTML",
            reply_markup=keyboards.start()
        )
    await state.clear()