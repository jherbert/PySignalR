__all__ = ['Event']


class Event:
    def __init__(self):
        self.handlers = []

    def __iadd__(self, handler):
        """Registers a handler that will be invoked when the event is raised."""
        if handler not in self.handlers:
            self.handlers.append(handler)
        return self

    def __isub__(self, handler):
        """Removes the handler from being being invoked."""
        if handler in self.handlers:
            self.handlers.remove(handler)
        return self

    def fire(self, *args, **kwargs):
        """Invokes the target method"""
        for handler in self.handlers:
            handler(*args, **kwargs)
