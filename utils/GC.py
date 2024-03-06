from httpx import AsyncClient
from typing import List, Optional

import json, time

import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler('logs/errors_GigaChat.log')

file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s \n\n')
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

class GigaChat:
    def __init__(self, client_secret: str, client_id: str, scope: str):

        self.client = AsyncClient(verify=False)

        self.client_secret = client_secret
        self.client_id = client_id
        self.scope = scope

        self.base_url = "https://gigachat.devices.sberbank.ru/api/v1/"

        self.timer: Optional[float] = None
        self.access_token: Optional[str] = None

    async def auth(self)-> str:

        url="https://ngw.devices.sberbank.ru:9443/api/v2/oauth"

        headers = {
            'Authorization': f'Basic {self.client_secret}',
            'RqUID': self.client_id,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        data = {
            'scope': self.scope
        }

        response = await self.client.post(url, headers=headers, data=data)
        return response.json()['access_token']

    async def get_token(self)-> str:

        if self.timer==None:
            self.timer = time.time()
            self.access_token = await self.auth()
        elif int(time.time()-self.timer)>1740:
            self.timer = time.time()
            self.access_token = await self.auth()

        return self.access_token

    async def get_tokens_count(self, _input: List[str]):

        url="tokens/count"

        headers = {
            'Authorization': f'Bearer {await self.auth()}',
            'Content-Type': 'application/json'
        }

        data = json.dumps(
            {
                'model': 'GigaChat',
                'input': _input
            }
        )
        try:
            response = await self.client.post(self.base_url+url, headers=headers, data=data)
            return response.json()
        except:
            logger.exception(ex)
            return False

    async def get_models(self):

        url="models"

        headers = {
            'Authorization': f'Bearer {await self.auth()}'
        }
        try:
            response = await self.client.get(self.base_url+url, headers=headers)
            return response.json()
        except:
            logger.exception(ex)
            return False


    async def chat(self, text: str):

        url="chat/completions"

        headers = {
            'Authorization': f'Bearer {await self.auth()}',
            'Content-Type': 'application/json'
        }

        data = json.dumps(
            {
                "model": "GigaChat:latest",
                "messages": [
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                "temperature": 1.6
            }
        )
        try:
            response = await self.client.post(self.base_url+url, headers=headers, data=data)
            return response.json()['choices'][0]['message']['content']
        except Exception:
            logger.exception(response.json())
            return False


    async def chat_storytelling(self,promt: str, text: str):

        url="chat/completions"

        headers = {
            'Authorization': f'Bearer {await self.auth()}',
            'Content-Type': 'application/json'
        }

        data = json.dumps(
            {
                "model": "GigaChat:latest",
                "messages": [
                    {
                        "role": "user",
                        "content": promt
                    },
                    {
                        "role": "assistant",
                        "content": "Понятно. Начнём?"
                    },
                    {
                        "role": "user",
                        "content": text
                    }
                ],
                "temperature": 1.6
            }
        )
        
        try:
            response = await self.client.post(self.base_url+url, headers=headers, data=data)
            return response.json()['choices'][0]['message']['content']
        except Exception:
            logger.exception(response.json())
            return False

    async def generate_image(self, promt: str):

        url="chat/completions"

        headers = {
            'Authorization': f'Bearer {await self.auth()}',
            'Content-Type': 'application/json'
        }

        data = json.dumps(
            {
                "model": "GigaChat:latest",
                "messages": [
                    {
                        "role": "user",
                        "content": promt
                    },
                ],
                "temperature": 0.7
            }
        )

        try:
            response = await self.client.post(self.base_url+url, headers=headers, data=data)
            return response
        except Exception as ex:
            logger.exception(ex)
            return False