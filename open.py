#!/usr/bin/python
from projectboard import ProjectBoard
DOOR_OPEN = 0 #GPIO status indocating an OPEN door.
DOOR_CLOSED = 1  #GPIO status indocating an CLOSED door.

P = ProjectBoard("GaragedeurBiezenhof")
P.sendpulse()
print("Pulse was sent to Realy - either to open or close the door")
