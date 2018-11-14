from unittest.mock import MagicMock

from pysignalr import Event

def test_method_1():
    return test_method_1.__name__

def test_method_2():
    return test_method_2.__name__

def test_method_3():
    return test_method_3.__name__ 

def test_should_add_handler():
    event = Event()
    event += test_method_1

    assert len(event.handlers) == 1

def test_should_not_add_duplicate():
    event = Event()
    event += test_method_1()
    event += test_method_1()

    assert len(event.handlers) == 1

def test_should_remove_handler():
    event = Event()
    event += test_method_1
    event += test_method_2
    event += test_method_3
    event -= test_method_1

    assert len(event.handlers) == 2

def test_should_fire_event():
    event = Event()
    test_result = MagicMock(return_value=True)
    
    event += test_result
    event.fire()

    assert test_result.called is True