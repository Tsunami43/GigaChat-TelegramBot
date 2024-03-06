from aiogram import Bot, Dispatcher
from data import BOT_TOKEN, ADMINS
from bot.handlers import append_account, main_handlers, setting_account, setting_promt
from aiogram.utils.markdown import hide_link

bot = Bot(token=BOT_TOKEN)

dp = Dispatcher()
dp.include_routers(
    append_account.router,
    main_handlers.router,
    setting_account.router,
    setting_promt.router
)


async def run():
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


async def message_for_admins(text: str):
    for admin in ADMINS:
        await bot.send_message(
            chat_id=admin,
            text=text,
            parse_mode="HTML"
        )
async def push_for_admins(name: str, url: str, title: str, text: str=None):
    if text==None:
        txt=f'Аккаунт {name} оставил реакцию!\n\nВ группе: {title}\n\n<a href="{url}"><b>Ссылка на реакцию</b></a>'
    else:
        txt=f'Аккаунт {name} оставил комментарий!\n\nВ группе: {title}\n\nКомментарий: {text}\n\n<a href="{url}"><b>Ссылка на комментарий</b></a>'
    for admin in ADMINS:
        await bot.send_message(
            chat_id=admin,
            text=txt,
            parse_mode="HTML"
        )