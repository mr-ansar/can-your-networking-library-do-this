import ansar.connect as ar

from quick_chat_api import *


I_AM = 'flash'

# The client object.
class QuickClient(ar.Point, ar.Stateless):
    def __init__(self, settings):
        ar.Point.__init__(self)
        ar.Stateless.__init__(self)
        self.settings = settings
        self.client = None

def QuickClient_Start(self, message):         # Start the networking.
    host = self.settings.host
    port = self.settings.port
    ipp = ar.HostPort(host, port)
    ar.connect(self, ipp)

def QuickClient_NotConnected(self, message):  # No networking.
    self.complete(message)

def QuickClient_Connected(self, message):
    self.send(Hello(i_am=I_AM), self.return_address)

def QuickClient_Welcome(self, message):
    name = message.to_you
    if name == I_AM:
        self.complete(ar.Ack())
    self.complete(ar.Nak())

def QuickClient_Stop(self, message):
    self.complete(ar.Aborted())

#
CLIENT_DISPATCH = [
    ar.Start,
    ar.NotConnected,
    ar.Connected,
    Welcome,
    ar.Stop,
]

ar.bind(QuickClient, CLIENT_DISPATCH)

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
factory_settings = Settings(host='127.0.0.1', port=5055)

if __name__ == '__main__':
    ar.create_object(QuickClient, factory_settings=factory_settings)
