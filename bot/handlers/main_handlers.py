from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.filters.state import State, StatesGroup, StateFilter
from aiogram.fsm.context import FSMContext

from bot.filters import Admin
from bot import keyboards
from bot import bot

from utils.session import Account
import data

from asyncio import sleep

router = Router()


@router.message(Admin(), StateFilter(None), Command('start'))
async def _start(message: Message):
    await message.answer(
        text=
            "<b>Список комманд:</b>\n\n"+
            "▶️ Запустить - <i>запуск комментирования</i>\n\n"+
            "⏹ Остановить - <i>остановить комментирование</i>\n\n"+
            "➕ Добавить аккаунт - <i>добавить аккаунт</i>",
        parse_mode="HTML",
        reply_markup=keyboards.start()
    )

@router.message(Admin(), StateFilter(None), F.text=="❌ Отменить действие")
async def _append(message: Message, state: FSMContext):
    await state.clear()
    data.CODE_INPUT=None
    data.CODE_WAIT=True
    data.TFA=None
    await message.answer(
        text=
            "<b>Список комманд:</b>\n\n"+
            "▶️ Запустить - <i>запуск комментирования</i>\n\n"+
            "⏹ Остановить - <i>остановить комментирование</i>\n\n"+
            "➕ Добавить аккаунт - <i>добавить аккаунт</i>",
        parse_mode="HTML",
        reply_markup=keyboards.start()
    )

@router.message(Admin(), StateFilter(None), F.text=="▶️ Запустить")
async def start_commenting(message: Message):
    if data.isBlockedComm:
        await message.answer(
            "<b><i>Комментинг уже запущен !</i></b>",
            parse_mode="HTML"
        )
    else:
        data.isBlockedComm=True
        await message.answer(
            "<b><i>Запуск комментинга...</i></b>",
            parse_mode="HTML"
        )

        clients = []
        clients_error = {}
        config = data.read_setting()['Setting_account']
        for session in data.init_sessions():
            client = Account(name=session)
            if await client.check_account():
                setting = await client.start(config=config)
                if setting!=False:
                    clients.append(client)
                    await message.answer(
                        text=
                            f"{client.name} настройки:\n\n"+
                            f"Задержка перед отправкой - {setting.sleep} секунд\n\n"+
                            f"Пропуск сообщений в чатах - {setting.skip_msg}\n\n"+
                            f"Пропуск постов - {setting.skip_post}\n\n"+
                            f"Задержка между сообщениями - {setting.skip_timeframe} секунд\n\n"+
                            f"Рабочее время - c {setting.work_time} часов\n\n"+
                            f"Эмоджи - {setting.emodji}\n\n"
                    )
                else:
                    clients_error[session]="сессия работает не корректно !"
            else:
                clients_error[session]="сессия не идентифицированна !"

        text = f"Отчет о запуске:\n\nЗапущено - <b>{len(clients)}</b> из <b>{len(clients)+len(clients_error)}</b>\n\n"
        if len(clients_error)==0:
            text = text+"Справка об аккаунтах с ошибками: <b>None</b>"
        else:
            text = text+"Справка об аккаунтах с ошибками:\n\n"
            for client in clients_error:
                text = text + f"{client} - {clients_error[client]}\n"
        await message.answer(
            text = text,
            parse_mode="HTML"
        )

        await bot.message_for_admins("✅ <b><i>COMMENTING ON</i></b>")

        data.COMMENTING=True
        while data.COMMENTING:
            await sleep(1)
        
        for client in clients:
            await client.stop_account()
        await bot.message_for_admins("🛑 <b><i>COMMENTING OFF</i></b>")
        data.isBlockedComm=False
        
        
        


@router.message(Admin(), StateFilter(None), F.text=="⏹ Остановить")
async def stop_commenting(message: Message):
    if data.COMMENTING:
        data.COMMENTING = False
        await message.answer(
            "<b><i>Отключение комментинга...</i></b>",
            parse_mode="HTML"
        )
    else:
        await message.answer(
            "<b><i>Комментинг уже выключен !</i></b>",
            parse_mode="HTML"
        )

@router.message(Admin(), StateFilter(None), F.text=="⚙️ Параметры комментирования")
async def setting_account(message: Message):
    setting = data.read_setting()["Setting_account"]
    await message.answer(
        text=
            f"Задержка <b>Х</b> перед отправкой сообщения = от <b>{setting['sleep_start']}</b> до <b>{setting['sleep_end']}</b> секунд <i>(выбирается рандомно)</i>",
        parse_mode="HTML",
        reply_markup=keyboards.setting_sleep()
    )
    await message.answer(
        text=
            f"Оставлять сообщение при каждом <b>Х</b> комментари в чате/группе = от <b>{setting['skip_msg_start']}</b> до <b>{setting['skip_msg_end']}</b> <i>(выбирается рандомно)</i>",
        parse_mode="HTML",
        reply_markup=keyboards.setting_skip_msg()
    )
    await message.answer(
        text=
            f"Оставлять комментарии к каждому <b>Х</b> посту = от <b>{setting['skip_post_start']}</b> до <b>{setting['skip_post_end']}</b> <i>(выбирается рандомно)</i>",
        parse_mode="HTML",
        reply_markup=keyboards.setting_skip_post()
    )
    await message.answer(
        text=
            f"Промежуток между отправкой сообщений = от <b>{setting['skip_timeframe_start']}</b> до <b>{setting['skip_timeframe_end']}</b> секунд <i>(выбирается рандомно)</i>",
        parse_mode="HTML",
        reply_markup=keyboards.setting_skip_timeframe()
    )
    await message.answer(
        text=
            f"Рабочее время аккаунта = c <b>{setting['work_time_start']}</b> до <b>{setting['work_time_end']}</b> часов по МСК",
        parse_mode="HTML",
        reply_markup=keyboards.setting_work_time()
    )
    await message.answer(
        text=
            f"Оставлять эмодзи, если в посте нет текста = <b>{setting['emodji']}</b>",
        parse_mode="HTML",
        reply_markup=keyboards.setting_emodji()
    )