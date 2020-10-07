#!/usr/bin/python

from datetime import datetime
import logging
import time
from time import sleep
from GSMModemClass import GSMModem
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
#
#LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
#LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

ALERT_OPEN_DOOR = 180 #300 After door closure pulse, when more then ALERT_OPEN_DOOR seconds elpased and door is still open issue ALERT.
MAX_OPEN_TIME = 120 #180 If door magnet detects door is open for MAX_OPEN_TIME, door gets shut automaticaly.
DOOR_OPEN = 0 #GPIO status indocating an OPEN door.
DOOR_CLOSED = 1  #GPIO status indocating an CLOSED door.
LOOP_SLEEP = 3 # Check the status every LOOP_SLEEP seconds.
MODEM_INIT_ATTEMPTS = 5

#disp = lcd()
logging.basicConfig(
  level=logging.INFO,
  filename="/home/pi/Logs/BiezenhofGarage.log",
  format="%(asctime)s %(message)s",
  datefmt='%a %d/%m/%Y %H:%M:%S',
  filemode="w")
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

errcntr = 0
notification = False
modeminit = False
modem = None
logging.info("Initialisation of the modem in progress.")
while errcntr < MODEM_INIT_ATTEMPTS:
  sleep(5)
  try:
    modem = GSMModem()
    modeminit = True
    logging.info("Modem initialisation SUCCESS.")
    break
  except:
    errcntr = errcntr + 1
    logging.error("Failed attempt [%i] to initialise the modem likely no access to ttyUSB0!" % errcntr)

now = datetime.now()
#disp.lcd_string("Garage poort",LCD_LINE_1)
#disp.lcd_string( str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) ,LCD_LINE_2)

start = time.time()
lastopen = datetime.now()
showlastopen = True
dooropenalreadynotified = False
P = ProjectBoard("GaragedeurBiezenhof")
smshandler = smsmessagehandler(5)

logging.info("Now waiting for events . . .")
while True:
  P.blinkgreen()
  doorstatus = P.getdoorstatus()
  # 1 indicates door is closed
  # 0 indicates door is open
  if doorstatus == DOOR_CLOSED:
    logging.debug("Door is closed")
    P.red_off();
    if (showlastopen):
      #disp.lcd_string("Poort last open",LCD_LINE_1)
      #disp.lcd_string(lastopen.strftime("%d%b%Y %H:%M"),LCD_LINE_2)
      showlastopen = False
    #logging.info("Door is closed. Reset timer.")
    start = time.time()
    dooropenalreadynotified = False
  else:
    elapsed = time.time() - start
    if (not dooropenalreadynotified) and (notification):
      modem.sendMessage('+32471569206',"NOTIFICATION: The garage door has just been opened.")
      logging.info("Notification has been sent for door being opened.")
      dooropenalreadynotified = True
    #disp.lcd_string("Door is open !",LCD_LINE_1)
    logging.info("Door has been open for %i seconds and will close in %i seconds." % (elapsed, MAX_OPEN_TIME - elapsed))
    #Red led goes ON the door is confirmed closed.
    P.red_on();
    if elapsed > MAX_OPEN_TIME:
      logging.info("Door was open for %i seconds. Pulse is sent." % elapsed)
      #disp.lcd_string("Auto closure",LCD_LINE_1)
      #disp.lcd_string(datetime.now().strftime("%d%b%Y %H:%M"),LCD_LINE_2)
      P.sendpulse()
      startclosing = time.time()
      doorstatus = P.getdoorstatus()
      # 1 indicates door is closed
      # 0 indicates door is open
      while doorstatus == DOOR_OPEN:
        P.blinkred(20)
        if smshandler.ready:
          smshandler.treatsmsmessages()
        doorstatus = P.getdoorstatus()
        elapsedclosing = time.time() - startclosing
        logging.info("Door is been closing for %i seconds." % elapsedclosing)
        if (elapsedclosing > ALERT_OPEN_DOOR):
          modem.sendMessage('+32471569206',"ALERT Biezenhof Garagedeur open over 5 minutes. New alert in 5 minutes.")
          startclosing = time.time()
      start = time.time()
      logging.info("Resume waiting for events . . .")
    lastopen = datetime.now()
    showlastopen = True
  sleep(LOOP_SLEEP)
  P.blinkgreen()
  # If there is a modem attached, we check if there is a message on the SIM card.
  if smshandler.ready:
    smshandler.treatsmsmessages()
    notification = smshandler.notification