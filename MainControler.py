#!/usr/bin/python

from datetime import datetime
import logging
import time
from time import sleep
from projectboard import ProjectBoard
from MessageHandler import smsmessagehandler

# import sqlite3
# from datetime import datetime
# from PDUClass import GSMMessage
# from LCDClass import lcd

# This is an endless loop that will check
# - if an SMS message comes in and is valid
# - if valid pulses the Relay to open the door or replies with SMS according to incoming message.
# - verifies how long the door has been open and when threshold is reached pulses the Relay
#   to close the door.
# Close door detection will reset openduration.
# Detection for door open will be done by a magnet contact
# Pulsing is done by a relay.
# Optional regular SMS sending to indicate system is operational
# Suggestion : every 100 times the door open an SMS is sent to Yves'mobile.
ALERT_OPEN_DOOR = 180 #300 After door closure pulse, when more then ALERT_OPEN_DOOR seconds elpased and door is still open issue ALERT.
MAX_OPEN_TIME = 120 #180 If door magnet detects door is open for MAX_OPEN_TIME, door gets shut automaticaly.
DOOR_OPEN = 0 #GPIO status indocating an OPEN door.
DOOR_CLOSED = 1  #GPIO status indocating an CLOSED door.
LOOP_SLEEP = 1 # Check the status every LOOP_SLEEP seconds.
MODEM_INIT_ATTEMPTS = 5

#disp = lcd()
logging.basicConfig(
  level=logging.DEBUG,
  filename="/home/pi/Logs/BiezenhofGarage.log",
  format="%(levelname)s %(asctime)s %(message)s",
  datefmt='%a %d/%m/%Y %H:%M:%S',
  filemode="w")
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)
logging.info("===  START OF PROGRAM ===")
logging.info("Loggers have been initiated.")
lastlooplog = ['Holds most recent loop']

notification = False
now = datetime.now()
nbrloops = 0
start = time.time()
lastopen = datetime.now()
showlastopen = True
dooropenalreadynotified = False
doorclosedalreadynotified = True
try:
  P = ProjectBoard("GaragedeurBiezenhof")
  # Note that messagehandler uses the Projectboard P.
  smshandler = smsmessagehandler(5,P)
except Exception:
  logging.exception("Failure to initialise hardware.")

logging.info("Now waiting for events . . .")
while True:
  lastlooplog.clear()
  lastlooplog.append('Loop starts at %s' % datetime.now())
  P.blinkgreen()
  doorstatus = P.getdoorstatus()
  # 1 indicates door is closed
  # 0 indicates door is open
  if doorstatus == DOOR_CLOSED:
    lastlooplog.append("The door is Closed")
    if not doorclosedalreadynotified:
      logging.info("The door has just been closed.")
      lastlooplog.append("The door was just closed")
      doorclosedalreadynotified = True
    P.red_off();
    if (showlastopen):
      showlastopen = False
    logging.debug("Door is closed. Reset timer.")
    start = time.time()
    dooropenalreadynotified = False
  else: # The door is OPEN
    lastlooplog.append("The door is Open")
    doorclosedalreadynotified = False
    elapsed = time.time() - start
    if not dooropenalreadynotified:
      if notification:
        lastlooplog.append("Open notification is sent")
        logging.info("The door has just been opened. SMS notification is sent")
        smshandler.sendmessage('+32471569206',"NOTIFICATION: The garage door has just been opened.")
      else:
        logging.info("The door has just been opened. No notification is sent")
        lastlooplog.append("No open notification is sent")
      dooropenalreadynotified = True
    #Red led goes ON the door is confirmed closed.
    P.red_on();
    if elapsed > MAX_OPEN_TIME:
      lastlooplog.append("Door has been open for too long. Automatic closure.")
      logging.info("Door was open for %i seconds. Pulse is sent to close the door." % elapsed)
      P.sendpulse()
      startclosing = time.time()
      doorstatus = P.getdoorstatus()
      # 1 indicates door is closed
      # 0 indicates door is open
      while doorstatus == DOOR_OPEN:
        lastlooplog.append("Waiting for door closure")
        logging.info("Waiting for the door to be closed...")
        P.blinkred(60)
        if smshandler.ready:
          lastlooplog.append("SMS Modem reports OK")
          smshandler.treatsmsmessages()
        else:
          lastlooplog.append("SMS Modem reports NOT OK")
          logging.error("The smshanlder reports not ready!")
        elapsedclosing = time.time() - startclosing
        if (elapsedclosing > ALERT_OPEN_DOOR):
          lastlooplog.append("ALLERT was sent - abnormal long open door.")
          smshandler.sendmessage('+32471569206',"ALERT Garagedeur open over 5 minutes. Attempting to close... New alert in 5 minutes.")
          P.sendpulse()
          startclosing = time.time()
        doorstatus = P.getdoorstatus()
      start = time.time()
      logging.info("Door took %i seconds to close." % elapsedclosing)
      logging.info("Resume waiting for events . . .")
    lastopen = datetime.now()
    showlastopen = True
  P.blinkgreen()
  if not smshandler.modem.getStatus():
    logging.error("Modem is NOT OK !!! Please check.")
    lastlooplog.append("SMS Modem reports NOT OK ")
  # If there is a modem attached, we check if there is a message on the SIM card.
  if smshandler.ready:
    smshandler.treatsmsmessages()
    if smshandler.messagetreated:
      lastlooplog.append("An SMS was received and handled.")
      logging.info("An SMS message was received, and treated.")
    notification = smshandler.notification
  else:
    logging.error("The smshanlder reports not ready!")
  if (nbrloops % 300) == 0:
      logging.info("counting loops %i " % nbrloops)
  nbrloops += 1
  lastlooplog.append("This ends loop %i" % nbrloops)
  with open("LastLoopLog.txt", "w") as f:
    for x in lastlooplog:
      f.write(x + "\r\n")
  sleep(LOOP_SLEEP)
