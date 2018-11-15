from typing import Union

from .common import CLOSE_MESSAGE_TYPE, PING_MESSAGE_TYPE, INVOCATION_MESSAGE_TYPE


class HubMessage:
    pass


class PingMessage(HubMessage):
    def __init__(self):
        self.type = PING_MESSAGE_TYPE


class CloseMessage(HubMessage):
    def __init__(self, error: Union[None, str] = None):
        self.error = error
        self.type = CLOSE_MESSAGE_TYPE


class HubInvocationMessage(HubMessage):
    def __init__(self, invocationId: str):
        self.invocationId = invocationId
        self.type = INVOCATION_MESSAGE_TYPE


class HubMethodInvocationMessage(HubInvocationMessage):
    def __init__(self, invocationId: str, target: str, arguments: []):
        super().__init__(invocationId)

        self.target = target
        self.arguments = arguments


class InvocationMessage(HubMethodInvocationMessage):
    def __init__(self, invocationId, target, arguments):
        super().__init__(invocationId, target, arguments)
