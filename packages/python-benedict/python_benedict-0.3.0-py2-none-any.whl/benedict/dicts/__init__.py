# -*- coding: utf-8 -*-

from benedict.dicts.keypath import KeypathDict
# from benedict.dicts.io import IODict
from benedict.dicts.parse import ParseDict

import copy
# import json


class benedict(KeypathDict, ParseDict):

    def __init__(self, *args, **kwargs):
        super(benedict, self).__init__(*args, **kwargs)

    def __getattribute__(self, name):
        attr = super(benedict, self).__getattribute__(name)
        if name.startswith('_'):
            return attr
        elif hasattr(attr, '__call__'):
            # print(attr, name)
            def attr_wrapper(*args, **kwargs):
                value = attr(*args, **kwargs)
                return benedict._cast(value)
            return attr_wrapper
        else:
            return attr

    def __getitem__(self, key):
        return benedict._cast(
            super(benedict, self).__getitem__(key))

    @staticmethod
    def _cast(value):
        if isinstance(value, dict) and not isinstance(value, benedict):
            return benedict(value)
        else:
            return value

    def deepcopy(self):
        return copy.deepcopy(self)

    @classmethod
    def fromkeys(cls, sequence, value=None):
        return benedict._cast(
            KeypathDict.fromkeys(sequence, value))

    # def print_items(self):
    #     default = lambda o: \
    #         o.isoformat() if isinstance(o, (datetime.date, datetime.datetime)) else str(o)
    #     print(json.dumps(self, indent=4, sort_keys=True, default=default))

    # def print_keypaths(self):
    #     default = lambda o: \
    #         o.isoformat() if isinstance(o, (datetime.date, datetime.datetime)) else str(o)
    #     print(json.dumps(self.keypaths(), indent=4, sort_keys=False, default=default))

