import ansar.connect as ar

from quick_chat_api import *

# The server object.
class Instructor(ar.Point, ar.Stateless):
    def __init__(self, settings):
        ar.Point.__init__(self)
        ar.Stateless.__init__(self)
        self.settings = settings

def Instructor_Start(self, message):         # Start the networking.
    host = self.settings.host
    port = self.settings.port
    ipp = ar.HostPort(host, port)
    ar.listen(self, ipp)

def Instructor_NotListening(self, message):  # No networking.
    self.complete(message)

def Instructor_Hello(self, message):
    name = message.i_am
    self.reply(Welcome(to_you=name))

def Instructor_Stop(self, message):          # Control-c or software interrupt.
    self.complete(ar.Aborted())

# Declare the messages expected by the server object.
INSTRUCTOR_DISPATCH = [
    ar.Start,
    ar.NotListening,
    Hello,
    ar.Stop,
]

ar.bind(Instructor, INSTRUCTOR_DISPATCH)

# Configuration for this executable.
class Settings(object):
    def __init__(self, host=None, port=None):
        self.host = host
        self.port = port

SETTINGS_SCHEMA = {
    'host': str,
    'port': int,
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

# Define default configuration and start the server.
factory_settings = Settings(host='127.0.0.1', port=5057)

if __name__ == '__main__':
    ar.create_object(Instructor, factory_settings=factory_settings)
