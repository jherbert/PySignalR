class HubMessage:
    pass


class PingMessage(HubMessage):
    pass


class HubInvocationMessage(HubMessage):
    def __init__(self, invocationId: str):
        self.invocationId = invocationId


class HubMethodInvocationMessage(HubInvocationMessage):
    def __init__(self, invocationId: str, target: str, arguments: []):
        super().__init__(invocationId)

        self.target = target
        self.arguments = arguments


class InvocationMessage(HubMethodInvocationMessage):
    def __init__(self, invocationId, target, arguments):
        super().__init__(invocationId, target, arguments)