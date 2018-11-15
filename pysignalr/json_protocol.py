# pylint: disable=unused-wildcard-import

import json

from .common import *
from .message import CloseMessage, HubMessage, InvocationMessage, PingMessage

__all__ = ['JsonProtocol']


class JsonProtocol:
    pass

    def parse_message(self, raw_message: str) -> HubMessage:
        if not raw_message:
            return

        message = json.loads(raw_message)

        invocationid = message.get('invocationId', None)
        message_type = message.get('type', None)
        target = message.get('target')
        arguments = message.get('arguments')

        hub_message = HubMessage()

        if message_type is None:
            return
        elif message_type == INVOCATION_MESSAGE_TYPE:
            hub_message = InvocationMessage(invocationid, target, arguments)
        elif message_type == PING_MESSAGE_TYPE:
            hub_message = PingMessage()
        elif message_type == CLOSE_MESSAGE_TYPE:
            error = message.get('error', None)
            hub_message = CloseMessage(error)

        return hub_message

    def write_message(self, message: HubMessage) -> str:

        json_message = ''

        if isinstance(message, InvocationMessage):
            json_message = json.dumps(message.__dict__) + JSON_RECORD_SEPARATOR

        return json_message