# pylint: disable=unused-wildcard-import

import json

from .common import *
from .message import HubMessage, InvocationMessage, PingMessage

__all__ = ['JsonProtocol']


class JsonProtocol:
    pass

    def parse_message(self, raw_message: str) -> HubMessage:
        if raw_message is None:
            return

        # JSON payloads are terminated 0x1e character
        raw_message = raw_message.replace(JSON_RECORD_SEPARATOR, '')

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

        return hub_message

    def write_message(self, message: HubMessage) -> str:
        return ''