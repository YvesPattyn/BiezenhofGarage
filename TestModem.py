#!/usr/bin/python

from GSMModemClass import GSMModem
import logging
from PDUClass import GSMMessage

logging.basicConfig(
  level=logging.INFO,
  format="%(levelname)s %(asctime)s %(message)s",
  datefmt='%a %d/%m/%Y %H:%M:%S')
logging.info("Initialisation process of the modem")
modem = GSMModem()
logging.info("Retrieving number of messages from modem")
msgNumbers = modem.getMessageNumbers()
logging.info(msgNumbers)
for msgNr in msgNumbers:
  msg = modem.readMessage(msgNr)
  logging.info("Message %i = %s" % (msgNr, msg))
  readablemsg = GSMMessage(msg)
  logging.info("Message: %s " % readablemsg.getMessage())
  logging.info("Received from %s " % readablemsg.OANum)