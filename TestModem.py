#!/usr/bin/python

from GSMModemClass import GSMModem
import logging

logging.basicConfig(
  level=logging.DEBUG,
  format="%(levelname)s %(asctime)s %(message)s",
  datefmt='%a %d/%m/%Y %H:%M:%S')
modem = GSMModem()
msgNumbers = modem.getMessageNumbers()
logging.info("MessageNumbers in modem")
logging.info(msgNumbers)