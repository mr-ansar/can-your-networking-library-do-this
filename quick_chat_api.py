import ansar.connect as ar

__all__ = [
    'Hello',
    'Welcome',
    'QuickChatClient',
    'QuickChatServer',
    'quick_server',
]

# Declare the API.
class Hello(object):
    def __init__(self, i_am='anonymous'):
        self.i_am = i_am

class Welcome(object):
    def __init__(self, to_you='anonymous'):
        self.to_you = to_you

ar.bind(Hello)
ar.bind(Welcome)


# The client object.
class QuickChatClient(ar.Point, ar.Stateless):
    def __init__(self, name, frequency=0.75, lifetime=5.0, remote_address=None):
        ar.Point.__init__(self)
        ar.Stateless.__init__(self)
        self.name = name
        self.frequency = frequency
        self.lifetime = lifetime
        self.remote_address = remote_address

def QuickChatClient_Start(self, message):
    self.start(ar.T1, seconds=self.frequency, repeating=True)
    self.start(ar.T2, seconds=self.lifetime)

    self.send(Hello(i_am=self.name), self.remote_address)

def QuickChatClient_T1(self, message):
    self.send(Hello(self.name), self.remote_address)

def QuickChatClient_Welcome(self, message):
    name = message.to_you
    self.test(name == self.name, f'Welcome for someone else ({name})')

def QuickChatClient_T2(self, message):
    self.cancel(ar.T1)
    self.complete(ar.Ack())

def QuickChatClient_Stop(self, message):
    self.cancel(ar.T1)
    self.complete(ar.Aborted())

# Declare the messages expected by the server object.
QUICK_CHAT_CLIENT_DISPATCH = [
    ar.Start,
    ar.T1,
    Welcome,
    ar.T2,
    ar.Stop,
]

ar.bind(QuickChatClient, QUICK_CHAT_CLIENT_DISPATCH)

#
#
class QuickChatServer(ar.Point, ar.Stateless):
    def __init__(self):
        ar.Point.__init__(self)
        ar.Stateless.__init__(self)

def QuickChatServer_Start(self, message):
    pass

def QuickChatServer_Hello(self, message):
    name = message.i_am
    self.send(Welcome(to_you=name), self.return_address)

def QuickChatServer_Stop(self, message):
    self.complete(ar.Aborted())

#
QUICK_CHAT_SERVER_DISPATCH = [
    ar.Start,
    Hello,
    ar.Stop,
]

ar.bind(QuickChatServer, QUICK_CHAT_SERVER_DISPATCH)

#
#
def quick_server(self):
    while True:
        m = self.select(Hello, ar.Stop)
        if isinstance(m, ar.Stop):
            return ar.Aborted()
        name = m.i_am
        self.reply(Welcome(to_you=name))

ar.bind(quick_server)
