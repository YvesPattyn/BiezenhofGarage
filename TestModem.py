#!/usr/bin/python

from GSMModemClass import GSMModem
import logging

logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s %(asctime)s %(message)s",
  datefmt='%a %d/%m/%Y %H:%M:%S')
logging.info("Initialisation process of the modem")
modem = GSMModem()
logging.info("Retrieving number of messages from modem")
msgNumbers = modem.getMessageNumbers()
logging.info(msgNumbers)