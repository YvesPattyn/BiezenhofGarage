#!/usr/bin/python
from projectboard import ProjectBoard
DOOR_OPEN = 0 #GPIO status indocating an OPEN door.
DOOR_CLOSED = 1  #GPIO status indocating an CLOSED door.

P = ProjectBoard("GaragedeurBiezenhof")
doorstatus = P.getdoorstatus()
if doorstatus == DOOR_CLOSED:
  print("door is closed")
else:
  print("door is open")
