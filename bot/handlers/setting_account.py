from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext

from bot.filters import Admin
from bot import keyboards

import data

router = Router()

class Setting(StatesGroup):
    sleep_start=State()
    sleep_end=State()
    skip_msg_start=State()
    skip_msg_end=State()
    skip_post_start=State()
    skip_post_end=State()
    skip_timeframe_start=State()
    skip_timeframe_end=State()
    work_time_start=State()
    work_time_end=State()
    emodji=State()


@router.message(Admin(), StateFilter(Setting), F.text=="❌ Отменить действие")
async def cancel_setting(message: Message, state: FSMContext):
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

@router.callback_query(F.data=="sleep_start")
async def sleep_start_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(Setting.sleep_start)
    await call.message.answer(
        text=
            f"Задержка перед отправкой сообщения = от <b>X</b> до <b>{data.read_setting()['Setting_account']['sleep_end']}</b> секунд <i>(выбирается рандомно)</i>\n\n<b>Введите X:</b>",
        parse_mode="HTML",
        reply_markup=keyboards.cancel()
    )

@router.message(Setting.sleep_start, F.text)
async def sleep_start_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        try:
            data.write_setting_accounts("sleep_start", int(message.text))
            await message.answer(
                text="<b>Успешно!</b>\n<i>Чтобы изменения вступили в силу перезапустите комментинг.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        except:
            await message.answer(
                text="<b>Ошибка!</b>\n<i>Изменения не вступили в силу.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        await state.clear()
    else:
        await message.answer(
            text=
                "<b>Ошибка значения!</b> Попробуйте снова...",
            parse_mode="HTML",
            reply_markup=keyboards.cancel()
        )


@router.callback_query(F.data=="sleep_end")
async def sleep_end_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(Setting.sleep_end)
    await call.message.answer(
        text=
            f"Задержка перед отправкой сообщения = от <b>{data.read_setting()['Setting_account']['sleep_start']}</b> до <b>X</b> секунд <i>(выбирается рандомно)</i>\n\n<b>Введите X:</b>",
        parse_mode="HTML",
        reply_markup=keyboards.cancel()
    )

@router.message(Setting.sleep_end, F.text)
async def sleep_end_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        try:
            data.write_setting_accounts("sleep_end", int(message.text))
            await message.answer(
                text="<b>Успешно!</b>\n<i>Чтобы изменения вступили в силу перезапустите комментинг.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        except:
            await message.answer(
                text="<b>Ошибка!</b>\n<i>Изменения не вступили в силу.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        await state.clear()
    else:
        await message.answer(
            text=
                "<b>Ошибка значения!</b> Попробуйте снова...",
            parse_mode="HTML",
            reply_markup=keyboards.cancel()
        )


@router.callback_query(F.data=="skip_msg_start")
async def skip_msg_start_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(Setting.skip_msg_start)
    await call.message.answer(
        text=
            f"Оставлять сообщение при каждом комментари в чате/группе = от <b>X</b> до <b>{data.read_setting()['Setting_account']['skip_msg_end']}</b> <i>(выбирается рандомно)</i>\n\n<b>Введите X:</b>",
        parse_mode="HTML",
        reply_markup=keyboards.cancel()
    )

@router.message(Setting.skip_msg_start, F.text)
async def skip_msg_start_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        try:
            data.write_setting_accounts("skip_msg_start", int(message.text))
            await message.answer(
                text="<b>Успешно!</b>\n<i>Чтобы изменения вступили в силу перезапустите комментинг.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        except:
            await message.answer(
                text="<b>Ошибка!</b>\n<i>Изменения не вступили в силу.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        await state.clear()
    else:
        await message.answer(
            text=
                "<b>Ошибка значения!</b> Попробуйте снова...",
            parse_mode="HTML",
            reply_markup=keyboards.cancel()
        )


@router.callback_query(F.data=="skip_msg_end")
async def skip_msg_end_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(Setting.skip_msg_end)
    await call.message.answer(
        text=
            f"Оставлять сообщение при каждом комментари в чате/группе = от <b>{data.read_setting()['Setting_account']['skip_msg_start']}</b> до <b>X</b> <i>(выбирается рандомно)</i>\n\n<b>Введите X:</b>",
        parse_mode="HTML",
        reply_markup=keyboards.cancel()
    )

@router.message(Setting.skip_msg_end, F.text)
async def skip_msg_end_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        try:
            data.write_setting_accounts("skip_msg_end", int(message.text))
            await message.answer(
                text="<b>Успешно!</b>\n<i>Чтобы изменения вступили в силу перезапустите комментинг.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        except:
            await message.answer(
                text="<b>Ошибка!</b>\n<i>Изменения не вступили в силу.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        await state.clear()
    else:
        await message.answer(
            text=
                "<b>Ошибка значения!</b> Попробуйте снова...",
            parse_mode="HTML",
            reply_markup=keyboards.cancel()
        )


@router.callback_query(F.data=="skip_post_start")
async def skip_post_start_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(Setting.skip_post_start)
    await call.message.answer(
        text=
            f"Оставлять комментарии к каждому посту = от <b>X</b> до <b>{data.read_setting()['Setting_account']['skip_post_end']}</b> <i>(выбирается рандомно)</i>\n\n<b>Введите X:</b>",
        parse_mode="HTML",
        reply_markup=keyboards.cancel()
    )

@router.message(Setting.skip_post_start, F.text)
async def skip_post_start_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        try:
            data.write_setting_accounts("skip_post_start", int(message.text))
            await message.answer(
                text="<b>Успешно!</b>\n<i>Чтобы изменения вступили в силу перезапустите комментинг.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        except:
            await message.answer(
                text="<b>Ошибка!</b>\n<i>Изменения не вступили в силу.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        await state.clear()
    else:
        await message.answer(
            text=
                "<b>Ошибка значения!</b> Попробуйте снова...",
            parse_mode="HTML",
            reply_markup=keyboards.cancel()
        )


@router.callback_query(F.data=="skip_post_end")
async def skip_post_end_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(Setting.skip_post_end)
    await call.message.answer(
        text=
            f"Оставлять комментарии к каждому посту = от <b>{data.read_setting()['Setting_account']['skip_post_start']}</b> до <b>X</b> <i>(выбирается рандомно)</i>\n\n<b>Введите X:</b>",
        parse_mode="HTML",
        reply_markup=keyboards.cancel()
    )

@router.message(Setting.skip_post_end, F.text)
async def skip_post_end_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        try:
            data.write_setting_accounts("skip_post_end", int(message.text))
            await message.answer(
                text="<b>Успешно!</b>\n<i>Чтобы изменения вступили в силу перезапустите комментинг.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        except:
            await message.answer(
                text="<b>Ошибка!</b>\n<i>Изменения не вступили в силу.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        await state.clear()
    else:
        await message.answer(
            text=
                "<b>Ошибка значения!</b> Попробуйте снова...",
            parse_mode="HTML",
            reply_markup=keyboards.cancel()
        )


@router.callback_query(F.data=="skip_timeframe_start")
async def skip_timeframe_start_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(Setting.skip_timeframe_start)
    await call.message.answer(
        text=
            f"Промежуток между отправкой сообщений = от <b>X</b> до <b>{data.read_setting()['Setting_account']['skip_timeframe_end']}</b> секунд <i>(выбирается рандомно)</i>\n\n<b>Введите X:</b>",
        parse_mode="HTML",
        reply_markup=keyboards.cancel()
    )

@router.message(Setting.skip_timeframe_start, F.text)
async def skip_timeframe_start_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        try:
            data.write_setting_accounts("skip_timeframe_start", int(message.text))
            await message.answer(
                text="<b>Успешно!</b>\n<i>Чтобы изменения вступили в силу перезапустите комментинг.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        except:
            await message.answer(
                text="<b>Ошибка!</b>\n<i>Изменения не вступили в силу.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        await state.clear()
    else:
        await message.answer(
            text=
                "<b>Ошибка значения!</b> Попробуйте снова...",
            parse_mode="HTML",
            reply_markup=keyboards.cancel()
        )


@router.callback_query(F.data=="skip_timeframe_end")
async def skip_timeframe_end_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(Setting.skip_timeframe_end)
    await call.message.answer(
        text=
            f"Промежуток между отправкой сообщений = от <b>{data.read_setting()['Setting_account']['skip_timeframe_start']}</b> до <b>X</b> секунд <i>(выбирается рандомно)</i>\n\n<b>Введите X:</b>",
        parse_mode="HTML",
        reply_markup=keyboards.cancel()
    )

@router.message(Setting.skip_timeframe_end, F.text)
async def skip_timeframe_end_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        try:
            data.write_setting_accounts("skip_timeframe_end", int(message.text))
            await message.answer(
                text="<b>Успешно!</b>\n<i>Чтобы изменения вступили в силу перезапустите комментинг.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        except:
            await message.answer(
                text="<b>Ошибка!</b>\n<i>Изменения не вступили в силу.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        await state.clear()
    else:
        await message.answer(
            text=
                "<b>Ошибка значения!</b> Попробуйте снова...",
            parse_mode="HTML",
            reply_markup=keyboards.cancel()
        )


@router.callback_query(F.data=="work_time_start")
async def work_time_start_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(Setting.work_time_start)
    await call.message.answer(
        text=
            f"Рабочее время аккаунта = c <b>X</b> до <b>{data.read_setting()['Setting_account']['work_time_end']}</b> часов по МСК\n\n<b>Введите X:</b>",
        parse_mode="HTML",
        reply_markup=keyboards.cancel()
    )

@router.message(Setting.work_time_start, F.text)
async def work_time_start_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        try:
            data.write_setting_accounts("work_time_start", int(message.text))
            await message.answer(
                text="<b>Успешно!</b>\n<i>Чтобы изменения вступили в силу перезапустите комментинг.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        except:
            await message.answer(
                text="<b>Ошибка!</b>\n<i>Изменения не вступили в силу.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        await state.clear()
    else:
        await message.answer(
            text=
                "<b>Ошибка значения!</b> Попробуйте снова...",
            parse_mode="HTML",
            reply_markup=keyboards.cancel()
        )


@router.callback_query(F.data=="work_time_end")
async def work_time_end_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(Setting.work_time_end)
    await call.message.answer(
        text=
            f"Рабочее время аккаунта = c <b>{data.read_setting()['Setting_account']['work_time_start']}</b> до <b>X</b> часов по МСК\n\n<b>Введите X:</b>",
        parse_mode="HTML",
        reply_markup=keyboards.cancel()
    )

@router.message(Setting.work_time_end, F.text)
async def work_time_end_handler(message: Message, state: FSMContext):
    if message.text.isdigit():
        try:
            data.write_setting_accounts("work_time_end", int(message.text))
            await message.answer(
                text="<b>Успешно!</b>\n<i>Чтобы изменения вступили в силу перезапустите комментинг.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        except:
            await message.answer(
                text="<b>Ошибка!</b>\n<i>Изменения не вступили в силу.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        await state.clear()
    else:
        await message.answer(
            text=
                "<b>Ошибка значения!</b> Попробуйте снова...",
            parse_mode="HTML",
            reply_markup=keyboards.cancel()
        )


@router.callback_query(F.data=="emodji")
async def emodji_callback(call: CallbackQuery, state: FSMContext):
    await state.set_state(Setting.emodji)
    await call.message.answer(
        text=
            f"Оставлять эмодзи, если в посте нет текста = <b>X</b>\n\n<b>Введите X (Да или Нет):</b>",
        parse_mode="HTML",
        reply_markup=keyboards.cancel()
    )

@router.message(Setting.emodji, F.text)
async def emodji_handler(message: Message, state: FSMContext):
    if message.text.lower() in ['да', 'нет']:
        try:
            data.write_setting_accounts("emodji", message.text.strip())
            await message.answer(
                text="<b>Успешно!</b>\n<i>Чтобы изменения вступили в силу перезапустите комментинг.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        except:
            await message.answer(
                text="<b>Ошибка!</b>\n<i>Изменения не вступили в силу.</i>",
                parse_mode="HTML",
                reply_markup=keyboards.start()
            )
        await state.clear()
    else:
        await message.answer(
            text=
                "<b>Ошибка значения!</b> Попробуйте снова...",
            parse_mode="HTML",
            reply_markup=keyboards.cancel()
        )