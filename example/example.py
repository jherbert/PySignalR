import sys
import logging
import asyncio
import threading

from pysignalr import HubConnection

# Setup console logger
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

loop = asyncio.get_event_loop()


async def main():
    def client_connected(message: str):
        print(f'>> {message}')

    def receive_message(user: str, message: str):
        print(f'{user} says: {message}')

    connection = HubConnection('ws://localhost:5000/chatHub', loop)
    connection.on('ClientConnected', client_connected)
    connection.on('ReceiveMessage', receive_message)

    await connection.start_async()

    while True:
        message = await loop.run_in_executor(None, sys.stdin.readline)
        await connection.send_async('SendMessage', 'Python User', message)


try:
    loop.run_until_complete(main())
    loop.run_forever()
finally:
    loop.close()