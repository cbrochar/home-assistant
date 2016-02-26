"""
homeassistant.components.garage_door.myQ
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Support for myQ garage doors.

For more details about this platform, please refer to the documentation at
https://home-assistant.io/components/garage_door.myQ/
"""
import logging

from homeassistant.components.garage_door import GarageDoorDevice
from homeassistant.const import (
    STATE_CLOSED, STATE_OPEN, STATE_OPENING, STATE_CLOSING, STATE_UNKNOWN, STATE_STOPPED, SERVICE_CLOSE, SERVICE_OPEN,
    ATTR_ENTITY_ID)
import myqgarage as myq

'''REQUIREMENTS = ['myq-garage']'''

global token

def setup_platform(hass, config, add_devices, discovery_info=None):
    """ Sets up myq-garage"""
    import myqgarage as myq
    """myq.UNSERNAME = config.get('garage_door','username')
    myq.PASSWORD = config.get('garage_door','password')
    myq.BRAND = config.get('garage_door','brand')"""
    token = myq.get_token()
    
    if token is None:
        logging.getLogger(__name__).error(
                "Login Error"
                "Check your myqgarage configuration")
        return

    add_devices(MyQGarageDoorDevice(DOOR) for DOOR in myq.get_doors(token))

class MyQGarageDoorDevice(GarageDoorDevice):
    """ Represents a MyQ garage door. """

    def __init__(self, DOOR):
        self.DOOR = DOOR

    @property
    def unique_id(self):
        """ Returns the id of this myQ garage door """
        return "{}.{}".format(self.__class__, self.DOOR.id)

    @property
    def name(self):
        """ Returns the name of the garage door if any. """
        return self.DOOR.name

    def update(self):
        """ Update the state of the garage door. """
        return myq.update_door(self.DOOR.token,self.DOOR.id).state

    @property
    def is_closed(self):
        """ True if device is closed. """
        print ("Is Closed:" + myq.get_doorinstance(self.DOOR.id).state)
        return myq.get_doorinstance(self.DOOR.id).state == 'Closed'
    
    def is_closing(self):
        print (STATE_CLOSED)
        return STATE_CLOSING

    def close_door(self):
        """ Close the device. """
        myq.set_doorstate(self.DOOR.token,self.DOOR.name, 0)

    def open_door(self):
        """ Open the device. """
        myq.set_doorstate(self.DOOR.token,self.DOOR.name, 1)