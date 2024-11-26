import ansar.connect as ar

# The Component object.
class ControlTower(ar.Point, ar.Stateless):
    def __init__(self, settings):
        ar.Point.__init__(self)
        ar.Stateless.__init__(self)
        self.settings = settings
        self.table = None
        self.group = None

def ControlTower_Start(self, message):         # Start the networking.
    instructor_ipp = self.settings.instructor
    radio_ipp = self.settings.radio

    self.table = ar.GroupTable(
        instructor=ar.CreateFrame(ar.ConnectToAddress, instructor_ipp),
        radio=ar.CreateFrame(ar.ListenAtAddress, radio_ipp),
    )
    self.group = self.table.create(self)

def ControlTower_GroupUpdate(self, message):
    self.table.update(message)

def ControlTower_Completed(self, message):
    d = self.debrief(self.return_address)
    if isinstance(d, ar.OnCompleted):
        d(message.value)
        return

    # Table has terminated.
    self.complete(ar.Aborted())

def ControlTower_Stop(self, message):          # Control-c or software interrupt.
    self.send(message, self.group)

def ControlTower_Enquiry(self, message):
    f = ar.roll_call(self.table)
    if f:
        self.send(f, self.return_address)
        return

    self.send(ar.UseAddress(self.table.instructor), self.return_address)

# Declare the messages expected by the server object.
CONTROL_TOWER_DISPATCH = [
    ar.Start,
    ar.GroupUpdate,
    ar.Completed,
    ar.Stop,
	ar.Enquiry,
]

ar.bind(ControlTower, CONTROL_TOWER_DISPATCH)

# Configuration for this executable.
class Settings(object):
    def __init__(self, instructor=None, radio=None):
        self.instructor = instructor or ar.HostPort()
        self.radio = radio or ar.HostPort()

SETTINGS_SCHEMA = {
    'instructor': ar.UserDefined(ar.HostPort),
    'radio': ar.UserDefined(ar.HostPort),
}

ar.bind(Settings, object_schema=SETTINGS_SCHEMA)

# Define default configuration and start the server.
factory_settings = Settings(instructor=ar.HostPort('127.0.0.1', 5057),
    radio=ar.HostPort('127.0.0.1', 5058),
)

if __name__ == '__main__':
    ar.create_object(ControlTower, factory_settings=factory_settings)
