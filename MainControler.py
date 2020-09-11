import sys,json
import sqlite3
import datetime
import logging
import time
from datetime import datetime
from time import sleep
from GSMModemClass import GSMModem
from PDUClass import GSMMessage
from projectboard import ProjectBoard
from LCDClass import lcd
# This is an endless loop that will check
# - if an SMS message comes in and is valid
# - if valid pulses the Relay to open the door.
# - verifies how long the door has been open and when threshold is reached pulses the Relay
#   to close the door.
# Close door detection will reset openduration.
# Detection for door open will be done by a magnet contact
# Pulsing is done by a relay.
# Optional regular SMS sending to indicate system is operational
# Suggestion : every 100 times the door open an SMS is sent to Yves'mobile.
#
LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

disp = lcd()

logging.basicConfig(level=logging.INFO)
logging.info("Initialisation of the modem in progress.")
try:
    modem = GSMModem()
except:
    logging.error("Failed to initialise the modem. Must connect and configure for tty0 !")

now = datetime.now()
disp.lcd_string("Garage poort",LCD_LINE_1)
disp.lcd_string( str(now.hour) + ":" + str(now.minute) + ":" + str(now.second) ,LCD_LINE_2)

start = time.time()
lastopen = datetime.now()
showlastopen = True
#log("ProjectBoard initialisation STARTED. --")
P = ProjectBoard("Testboard")
logging.info("Starting listener...")
while True:
    doorstatus = P.getdoorstatus()
    # 1 indicates door is closed
    # 0 indicates door is open
    if (doorstatus == 1):
        if (showlastopen):
            disp.lcd_string("Poort last open",LCD_LINE_1)
            disp.lcd_string(lastopen.strftime("%d%b%Y %H:%M"),LCD_LINE_2)
            showlastopen = False
        #logging.info("Door is closed. Reset timer.")
        start = time.time()
    else:
        elapsed = time.time() - start
        disp.lcd_string("Door is open !",LCD_LINE_1)
        logging.debug("Door has been open for %i seconds. Check if closure required." % elapsed)
        if (elapsed > 20):
            logging.debug("Sending closure pulse")
            disp.lcd_string("Auto closure",LCD_LINE_1)
            disp.lcd_string(datetime.now().strftime("%d%b%Y %H:%M"),LCD_LINE_2)
            P.sendpulse()
            sleep(10)
            start = time.time()
        lastopen = datetime.now()
        showlastopen = True
    sleep(3)
    msg0 = modem.readMessage(0)
    try:
        readablemsg = GSMMessage(msg0)
        print("Message: %s " % readablemsg.getMessage())
        print("Received from %s " % readablemsg.OANum)
        # Get a the next message from the SIM
        if (readablemsg.OANum in ('+32471569200','+32471569201','+32471569206')):
            print("Phone number %s is authorised to send requests" % readablemsg.OANum)
            if ("OPEN" in readablemsg.getMessage()):
                print("Open order is now executed")
                P.sendpulse()
            else:
                print("'%s' is not a valid command" % readablemsg.getMessage())
        else:
            print("Phone number %s is authorised NOT to send requests" % readablemsg.OANum)
        msg0 = modem.deleteAllMessages()
    except:
        logging.debug("There is no message 0")
        
    #   if (message.text == "OPEN")
    #     doorstatus = P.getdoorstatus()
    #     1 indicates door is closed
    #     if (doorstatus == 1):
    #       logging.info("Sending pulse to open the door")
    #       P.sendpulse()


#P.sendpulse()
#sleep(3)
#P.relay_on()
#sleep(3)
#P.relay_off()
