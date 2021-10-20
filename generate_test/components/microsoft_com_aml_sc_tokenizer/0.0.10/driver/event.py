# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
""" This modules define a basic event handler.
    Don't use a event library to avoid installation of the dependency.
"""


class Event(list):
    """ The class is used to define an event and allow add/remove event hanlders."""

    def __call__(self, *args, **kwargs):
        """ Call all event handlers."""
        for fun in self:
            fun(*args, **kwargs)

    def __iadd__(self, handler):
        """ Append an event handler."""
        self.append(handler)
        return self

    def __isub__(self, handler):
        """ Remove an existing event handler from the list."""
        self.remove(handler)
        return self
