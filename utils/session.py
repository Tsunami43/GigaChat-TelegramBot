import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('logs/errors_session.log')

file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s \n\n')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


from pyrogram import Client
from pyrogram import filters
from pyrogram import errors
from pyrogram.errors import SessionPasswordNeeded, ApiIdInvalid, PhoneNumberInvalid, PhoneCodeInvalid, PhoneNumberBanned

from asyncio import sleep
from os import remove
import random
import data
import time
from datetime import datetime

from bot import bot

class Authorization:    

    def __init__(self, name: str, api_id: int=None, api_hash: str=None, phone: str=None, password: str=None)-> None:
        self.name: str = name
        self.api_id: int = api_id
        self.api_hash: str = api_hash
        self.phone: str = phone
        self.phone_code: str = None
        self.phone_code_hash: str = None
        self.password: str = password
        self.client: Client= None


    async def server_connect(self)->None:
        self.client=Client("sessions/"+self.name, self.api_id, self.api_hash)
        await self.client.connect()


    async def send_code(self)-> int:
        """
             1 - код отправлен
            10 - ошибка api
            11 - ошибка номера
            12 - номер заблокирован
             0 - другая ошибка
        """
        try:
            await self.server_connect()
            sCode = await self.client.send_code(self.phone)
            self.phone_code_hash = sCode.phone_code_hash
            return 1

        except ApiIdInvalid:
            await self.cancel_authorization()
            return 10

        except PhoneNumberInvalid:
            await self.cancel_authorization()
            return 11

        except PhoneNumberBanned:
            await self.cancel_authorization()
            return 12

        except Exception as ex:
            logger.exception(ex)
            await self.cancel_authorization()
            return 0

    async def check_code(self)-> int:
        """ 
             1 - вход выполнен
            10 - если для входа требуется (2fa)
            11 - недействительный код
             0 - если возникает ошибка
        """
        try:
            await self.client.sign_in(self.phone, phone_code=self.phone_code, phone_code_hash=self.phone_code_hash)
            await self.client.disconnect()

            data.write_account(
                name=self.name,
                api_id=self.api_id,
                api_hash=self.api_hash,
                phone=self.phone,
                tfa=self.password
            )

            return 1

        except SessionPasswordNeeded:
            return 10

        except PhoneCodeInvalid:
            logger.exception(ex)
            await self.cancel_authorization()
            return 11

        except Exception as ex:
            logger.exception(ex)
            await self.cancel_authorization()
            return 0


    async def check_password(self)-> bool:
        """
             1 - пароль верен -> авторизация успешна
            10 - пароль верен -> ошибка авторизации
             0 - пароль не верен
        """
        try:
            await self.client.check_password(self.password)
            match (await self.check_code()):
                case (1):
                    return 1
                case (_):
                    await self.cancel_authorization()
                    return 10

        except Exception as ex:
            logger.exception(ex)
            await self.cancel_authorization()
            return 0
    

    async def cancel_authorization(self)-> None:
        if self.client!=None:
            await self.client.disconnect()
            remove(f"sessions/{self.name}.session")


class Account:
    def __init__(self, name: str):
        self.name=name
        self.client = Client(
            "sessions/"+self.name
        )

    async def check_account(self)-> bool:
        
        try:
            await self.client.connect()

            try:
                await self.client.get_me()
            except (
                    errors.ActiveUserRequired,
                    errors.AuthKeyInvalid,
                    errors.AuthKeyPermEmpty,
                    errors.AuthKeyUnregistered,
                    errors.AuthKeyDuplicated,
                    errors.SessionExpired,
                    errors.SessionPasswordNeeded,
                    errors.SessionRevoked,
                    errors.UserDeactivated,
                    errors.UserDeactivatedBan,
                    ) as ex:
                logger.info(f"***Username account: {self.name}")
                logger.exception(f"|{self.name}|--->", msg=ex)
                await self.client.disconnect()
                return False
            else:
                await self.client.disconnect()
                return True

        except Exception as ex:
            logger.info(f"***Username account: {self.name}")
            logger.exception(ex)
            return False

        
    class Setting:
        def __init__(self, config):
            self.sleep = random.randint(config['sleep_start'], config['sleep_end'])
            self.skip_msg = random.randint(config['skip_msg_start'], config['skip_msg_end'])
            self.skip_post = random.randint(config['skip_post_start'], config['skip_post_end'])
            self.skip_timeframe = random.randint(config['skip_timeframe_start'], config['skip_timeframe_end'])
            self.work_time = range(config['work_time_start'], config['work_time_end']+1)
            self.emodji = config['emodji'].lower()=='да' and True or False
            self.timer_start = None
            self.chats={}

        def pause_timeframe(self)-> bool:
            if self.timer_start==None:
                self.timer_start = time.time()
                return True
            elif int(time.time()-self.timer_start)>=self.skip_timeframe:
                self.timer_start = time.time()
                return True
            else:
                return False

        def pause_worktime(self)-> bool:
            if datetime.now().hour in self.work_time:
                return True
            else:
                return False
        

        def filter(self, chat: str, target: str):
            if not chat in self.chats:
                self.chats[chat]=0
            
            match (target):
                case ('MESSAGE'):
                    if self.chats[chat]==self.skip_msg:
                        if self.pause_timeframe() and self.pause_worktime():
                            self.chats[chat]=0
                            return True
                        else:
                            return False 
                    else:
                        self.chats[chat]+=1
                        return False
                case ('POST'):
                    if self.chats[chat]==self.skip_post:
                        if self.pause_timeframe() and self.pause_worktime():
                            self.chats[chat]=0
                            return True
                        else:
                            return False 
                    else:
                        self.chats[chat]+=1
                        return False

                

    async def start(self, config: dict):
        
        await self.client.start()
        try:
            setting = self.Setting(config=config)
            # dialogs = self.client.get_dialogs()
            # async for dialog in dialogs:
            #     if dialog.chat.title=="Test Commenting":
            #         _id = dialog.chat.id

            #     if dialog.chat.title=="123":
            #         _id1 = dialog.chat.id
            # print(_id, _id1)

            reactions = ['🔥', '👍', '😎', '🤩', '🤯']
            

            @self.client.on_message(filters.group & filters.text)
            async def handler_message(client, message):
                try:
                    if setting.filter(chat=message.chat.title, target='MESSAGE'):
                        await self.client.read_chat_history(message.chat.id)
                        await sleep(setting.sleep)

                        if message.text!=None:

                            response = await data.GIGACHAT._chat_complection(
                                data.read_setting()['Promt'], message.text
                            )

                            if response!=False:
                                msg = await self.client.send_message(chat_id=message.chat.id, text=response)
                                await bot.push_for_admins(
                                    name=self.name,
                                    url=msg.link,
                                    text=response,
                                    title=message.chat.title
                                )
                        else:

                            if setting.emodji:
                                await self.client.send_reaction(
                                    chat_id=message.chat.id,
                                    message_id=message.id,
                                    emoji=random.choice(reactions)
                                )
                                await bot.push_for_admins(
                                    name=self.name,
                                    url=message.link,
                                    title=message.chat.title
                                )

                except Exception as ex:
                    logger.info(f"***Username account: {self.name}")
                    logger.exception(ex)


            @self.client.on_message(filters.group & (filters.photo | filters.voice | filters.audio | filters.document | filters.video ))
            async def handler_message(client, message):
                try:
                    if setting.filter(chat=message.chat.title, target='MESSAGE'):

                        await self.client.read_chat_history(message.chat.id)
                        await sleep(setting.sleep)

                        if message.caption!=None:

                            response = await data.GIGACHAT._chat_complection(
                                data.read_setting()['Promt'], message.caption
                            )

                            if response!=False:
                                msg = await self.client.send_message(chat_id=message.chat.id, text=response)
                                await bot.push_for_admins(
                                    name=self.name,
                                    url=msg.link,
                                    text=response,
                                    title=message.chat.title
                                )
                        
                        else:

                            if setting.emodji:
                                await self.client.send_reaction(
                                    chat_id=message.chat.id,
                                    message_id=message.id,
                                    emoji=random.choice(reactions)
                                )
                                await bot.push_for_admins(
                                    name=self.name,
                                    url=message.link,
                                    title=message.chat.title
                                )

                except Exception as ex:
                    logger.info(f"***Username account: {self.name}")
                    logger.exception(ex)

            @self.client.on_message(filters.channel & filters.text)
            async def handler_message(client, message):
                try:
                    if setting.filter(chat=message.chat.title, target='POST'):

                        await self.client.read_chat_history(message.chat.id)
                        await sleep(setting.sleep)

                        if message.text!=None:

                            response = await data.GIGACHAT._chat_complection(
                                data.read_setting()['Promt'], message.text
                            )

                            if response!=False:
                                # Get the discussion message
                                m = await self.client.get_discussion_message(message.chat.id, message.id)
                                msg = await m.reply(response)
                                await bot.push_for_admins(
                                    name=self.name,
                                    url=msg.link,
                                    text=response,
                                    title=message.chat.title 
                                )
                        else:

                            if setting.emodji:
                                await self.client.send_reaction(
                                    chat_id=message.chat.id,
                                    message_id=message.id,
                                    emoji=random.choice(reactions)
                                )
                                await bot.push_for_admins(
                                    name=self.name,
                                    url=message.link,
                                    title=message.chat.title
                                )

                except Exception as ex:
                    logger.info(f"***Username account: {self.name}")
                    logger.exception(ex)


            @self.client.on_message(filters.channel & (filters.photo | filters.voice | filters.audio | filters.document | filters.video ))
            async def handler_message(client, message):
                try:
                    if setting.filter(chat=message.chat.title, target='POST'):

                        await self.client.read_chat_history(message.chat.id)
                        await sleep(setting.sleep)

                        if message.caption!=None:

                            response = await data.GIGACHAT._chat_complection(
                                data.read_setting()['Promt'], message.caption
                            )

                            if response!=False:
                                # Get the discussion message
                                m = await self.client.get_discussion_message(message.chat.id, message.id)
                                msg = await m.reply(response)
                                await bot.push_for_admins(
                                    name=self.name,
                                    url=msg.link,
                                    text=response,
                                    title=message.chat.title
                                )
                        else:

                            if setting.emodji:
                                await self.client.send_reaction(
                                    chat_id=message.chat.id,
                                    message_id=message.id,
                                    emoji=random.choice(reactions)
                                )
                                await bot.push_for_admins(
                                    name=self.name,
                                    url=message.link,
                                    title=message.chat.title
                                )
                                
                except Exception as ex:
                    logger.info(f"***Username account: {self.name}")
                    logger.exception(ex)


            return setting

        except Exception as ex:
            await self.stop_account()
            logger.info(f"***Username account: {self.name}")
            logger.exception(ex)
            return False

    async def stop_account(self):
        await self.client.stop()