# WS client example
import logging
import asyncio

from pysignalr import HubConnection

# Setup console logger
#logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger()
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
logger.addHandler(ch)

loop = asyncio.get_event_loop()


def client_connected(message: str):
    print(f'>> {message}')


def receive_message(user: str, message: str):
    print(f'{user} says: {message}')


connection = HubConnection('ws://localhost:5000/chatHub', loop)
connection.on('ClientConnected', client_connected)
connection.on('ReceiveMessage', receive_message)

try:
    loop.run_until_complete(connection.start_async())
    loop.run_forever()
finally:
    loop.run_until_complete(connection.stop_async())
    loop.close()