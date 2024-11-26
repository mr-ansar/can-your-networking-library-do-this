import ansar.connect as ar

from quick_chat_api import *

# The server object.
class HelpDesk(ar.Point, ar.Stateless):
    def __init__(self, settings):
        ar.Point.__init__(self)
        ar.Stateless.__init__(self)
        self.settings = settings
        self.csr = None

def HelpDesk_Start(self, message):
    self.csr = self.create(quick_server)

    host = self.settings.host
    port = self.settings.port
    ipp = ar.HostPort(host, port)
    ar.listen(self, ipp)

def HelpDesk_NotListening(self, message):
    self.complete(message)

def HelpDesk_Enquiry(self, message):
    response = ar.AddressBook(address=self.csr)
    self.send(response, self.return_address)

def HelpDesk_Stop(self, message):
    self.send(message, self.quick_chat)

def HelpDesk_Completed(self, message):
    self.complete(message.value)

# Declare the messages expected by the server object.
SERVER_DISPATCH = [
    ar.Start,
    ar.NotListening,
    ar.Enquiry,
    ar.Stop,
	ar.Completed,
]

ar.bind(HelpDesk, SERVER_DISPATCH)

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
factory_settings = Settings(host='127.0.0.1', port=5056)

if __name__ == '__main__':
    ar.create_object(HelpDesk, factory_settings=factory_settings)
