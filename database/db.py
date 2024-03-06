import sqlite3
import logging
from datetime import datetime as dt


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('database/erros.log')

file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


class Database:

    def __init__(self, db_path: str="database/db.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.curs = self.conn.cursor()
        self.curs.execute("""
            CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            register TEXT
            )
            """)
        self.curs.execute("""
            CREATE TABLE IF NOT EXISTS Profile (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            chat_id INTEGER NOT NULL,
            balance INTEGER
            )
            """)
        self.conn.commit()

    def GetUser(self, chat_id: int)-> int:
        try:
            if self.curs.execute("""SELECT chat_id FROM Users 
                                 WHERE chat_id = '{}' """.format(chat_id)).fetchone()!=None:
                return 10
            else:
                return 11
        except Exception as ex:
            logger.exception(ex)
            return 0


    def AppendUser(self, chat_id: int, username: str=None, first_name: str=None, last_name: str=None)->bool:
        try:
            register = dt.now().strftime("%Y-%m-%d")
            self.curs.execute("""INSERT INTO Users (chat_id, username, first_name, last_name, register) 
                                VALUES ('{}', '{}', '{}', '{}', '{}')
                            """.format(chat_id, username, first_name, last_name, register))
            self.conn.commit()
            return 100
        except Exception as ex:
            logger.exception(ex)
            return 1000

    def AppendProfile(self, chat_id: int, balance: int=5):
        try:
            self.curs.execute("""INSERT INTO Profile (chat_id, balance) 
                                VALUES ('{}', '{}')
                                """.format(chat_id, balance))
            self.conn.commit()
            return 200
        except Exception as ex:
            logger.exception(ex)
            return 2000

    def CreateUser(self, chat_id: int, username: str=None, first_name: str=None, last_name: str=None)->bool:
        """
            10 - Пользователь найден
            11 - Пользователь не найден

            100 - Пользовател добавлен в базу
            101 - Пользователь есть в базе
            
            200 - Профиль пользователя создан
        
            0 - Ошибка поиска пользователя

            1000 - Пользователь не добавлен в базу

            2000 - Профиль пользователя не создан
        """

        match (self.GetUser(chat_id=chat_id)):
            case (11):
                match (self.AppendUser(chat_id=chat_id, username=username, first_name=first_name, last_name=last_name)):
                    case (100):
                        match (self.AppendProfile(chat_id=chat_id)):
                            case (200):
                                pass
                            case (2000):
                                pass
                    case (1000):
                        pass
            case (10):
                pass
            case (0):
                pass

db = Database()

# if __name__ == "__main__":
#     # db.default()
#     print(db.AppendUser(chat_id=1333, username="asdf"))