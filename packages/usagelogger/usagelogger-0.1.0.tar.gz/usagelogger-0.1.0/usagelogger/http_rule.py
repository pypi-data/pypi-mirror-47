# Copyright (c) 2016-2019, Resurface Labs Inc. All Rights Reserved.


class HttpRule(object):

    def __init__(self, verb, scope=None, param1=None, param2=None):
        self.verb = verb
        self.scope = scope
        self.param1 = param1
        self.param2 = param2
