import ansar.connect as ar

from quick_chat_api import *

# The server object.
I_AM = 'trainee'

class TraineePilot(ar.Point, ar.Stateless):
    def __init__(self, settings):
        ar.Point.__init__(self)
        ar.Stateless.__init__(self)
        self.settings = settings
        self.quick_chat = None

def TraineePilot_Start(self, message):
    host = self.settings.host
    port = self.settings.port
    ipp = ar.HostPort(host, port)
    ar.connect(self, ipp)

def TraineePilot_NotConnected(self, message):
    self.complete(message)

def TraineePilot_Connected(self, message):
    self.send(ar.Enquiry(), self.return_address)

def TraineePilot_UseAddress(self, message):
    self.server = message.address
    self.send(Hello(i_am=I_AM), self.server)

def TraineePilot_Welcome(self, message):
    name = message.to_you
    if name == I_AM:
        self.complete(ar.Ack())
    self.complete(ar.Nak())

def TraineePilot_Stop(self, message):
    self.complete(ar.Aborted())

# Declare the messages expected by the server object.
TRAINEE_PILOT_DISPATCH = [
    ar.Start,
    ar.NotConnected,
    ar.Connected,
    ar.UseAddress,
    Welcome,
    ar.Stop,
]

ar.bind(TraineePilot, TRAINEE_PILOT_DISPATCH)

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
factory_settings = Settings(host='127.0.0.1', port=5058)

if __name__ == '__main__':
    ar.create_object(TraineePilot, factory_settings=factory_settings)