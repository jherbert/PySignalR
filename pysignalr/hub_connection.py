import asyncio
import logging
import json
from typing import Callable

import websockets

from .common import HANDSHAKE_PROTOCOL, HANDSHAKE_VERSION, JSON_RECORD_SEPARATOR
from .event import Event
from .message import InvocationMessage
from .json_protocol import JsonProtocol

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

__all__ = ['HubConnection']


class HubConnection(object):
    def __init__(self, url: str, loop):
        self.url = url
        self.handlers = {}
        self.socket = None
        self.receive_task = None
        self.nextId = 1

        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop

        self.hub_protocol = JsonProtocol()
        self.receive_task = None

    def on(self, invocation: str, handler: Callable):
        if invocation not in self.handlers:
            self.handlers[invocation] = Event()
        self.handlers[invocation] += handler

    async def send_async(self, methodName: str, *args):
        if self.socket is None:
            return

        try:
            invocation_message = InvocationMessage(self.get_next_id(), methodName, args)
            writeable_message = self.hub_protocol.write_message(invocation_message)
            await self.socket.send(writeable_message)

        except asyncio.CancelledError:
            raise

        except Exception:
            logger.warning("Unexpected exception while processing outgoing messages", exc_info=True)

    async def start_async(self):
        socket = await websockets.connect(self.url)

        handshake = {'protocol': HANDSHAKE_PROTOCOL, 'version': HANDSHAKE_VERSION}
        handhake_payload = json.dumps(handshake) + JSON_RECORD_SEPARATOR
        await socket.send(handhake_payload)

        # TODO: Handle handshake response; should be a empty object
        await socket.recv()

        self.socket = socket

        # Receive Loop
        self.receive_task = asyncio.ensure_future(self.incoming_message_handler(), loop=self.loop)

    async def stop_async(self):
        # Cancel the receive loop
        if self.receive_task is not None:
            self.receive_task.cancel()

        # Close the socket
        if self.socket is not None:
            await self.socket.close()

    async def process_incoming(self, message):
        logger.debug(f'S-C-> {message}')
        for m in message.split(JSON_RECORD_SEPARATOR):
            hub_message = self.hub_protocol.parse_message(m)

            if type(hub_message) is InvocationMessage and hub_message.target in self.handlers:
                arguments = ','.join(hub_message.arguments)
                logger.debug(f'Raising event {hub_message.target} with arguments: {arguments}')

                self.handlers[hub_message.target].fire(*hub_message.arguments)

    async def incoming_message_handler(self):
        if self.socket is None:
            return

        try:
            async for message in self.socket:
                await self.process_incoming(message)

        except asyncio.CancelledError:
            raise

        except Exception:
            logger.warning("Unexpected exception while processing incoming messages", exc_info=True)

    def get_next_id(self) -> str:
        self.nextId += 1
        return str(self.nextId)