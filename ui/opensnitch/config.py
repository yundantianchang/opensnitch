import os
import json

class Config:
    __instance = None

    @staticmethod
    def init(filename):
        Config.__instance = Config(filename)
        return Config.__instance

    @staticmethod
    def get():
        return Config.__instance

    def __init__(self, filename):
        self.filename = os.path.abspath( os.path.expanduser(filename) )
        self.exists = os.path.isfile(self.filename)

        self.default_timeout = 15
        self.default_action = "allow"
        self.default_duration = "until restart"
        self.default_pingtime = 1
        self.default_pingtimeout = 3

        if self.exists:
            # print( "Loading configuration from %s ..." % self.filename )
            data = json.load(open(self.filename))

            self.default_timeout = data["default_timeout"]
            self.default_action  = data["default_action"]
            self.default_duration = data["default_duration"]
            self.default_pingtime = data["default_pingtime"]
            self.default_pingtimeout = data["default_pingtimeout"]
            if self.default_pingtime < 1:
                self.default_pingtime = 1
            if self.default_pingtimeout < 3 * self.default_pingtime:
                self.default_pingtimeout = self.default_pingtime * 3

    def save(self):
        dirname = os.path.dirname(self.filename)
        if os.path.isdir(dirname) == False:
            os.makedirs(dirname, exist_ok=True)

        with open(self.filename, 'w') as fp:
            data = {
                'default_timeout': self.default_timeout,
                'default_action': self.default_action,
                'default_duration': self.default_duration,
                'default_pingtime': self.default_pingtime,
                'default_pingtimeout': self.default_pingtimeout,
            }
            json.dump(data, fp)
            self.exists = True
