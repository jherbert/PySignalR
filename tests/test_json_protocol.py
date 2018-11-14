import pytest

from pysignalr.message import InvocationMessage, PingMessage
from pysignalr.json_protocol import JsonProtocol


@pytest.mark.parametrize(
    "test_input,expected",
    [
        # InvocationMessage_HasInvocationId
        ('{"type":1,"invocationId":"123","target":"Target","arguments":[1,"Foo",2.0]}', InvocationMessage('123', 'Target', [1, 'Foo', 2])),

        # InvocationMessage_HasFloatArgument
        ('{"type":1,"target":"Target","arguments":[1,"Foo",2.0]}', InvocationMessage(None, 'Target', [1, 'Foo', 2])),

        # InvocationMessage_HasBoolArgument
        ('{"type":1,"target":"Target","arguments":[true]}', InvocationMessage(None, 'Target', [True])),

        # InvocationMessage_HasNullArgument
        ('{"type":1,"target":"Target","arguments":[null]}', InvocationMessage(None, 'Target', [None])),

        # InvocationMessage_HasCustomArgumentWithNoCamelCase
        (
            '{"type":1,"target":"Target","arguments":[{"StringProp":"SignalR!","DoubleProp":6.2831853071,"IntProp":42,"DateTimeProp":"2017-04-11T00:00:00Z","ByteArrProp":"AQID"}]}',
            InvocationMessage(
                None, 'Target', [
                    {
                        'StringProp': 'SignalR!',
                        'DoubleProp': 6.2831853071,
                        'IntProp': 42,
                        'DateTimeProp': '2017-04-11T00:00:00Z',
                        'ByteArrProp': 'AQID'
                    }
                ]
            )
        )
    ]
)
def test_invocation_messages(test_input, expected):
    json_protocol = JsonProtocol()

    actual = json_protocol.parse_message(test_input)

    assert isinstance(actual, InvocationMessage)
    assert actual.target == expected.target
    assert actual.invocationId == expected.invocationId
    assert actual.arguments == expected.arguments


def test_ping_message():
    json_protocol = JsonProtocol()
    json = '{"type":6}'

    actual = json_protocol.parse_message(json)

    assert isinstance(actual, PingMessage)