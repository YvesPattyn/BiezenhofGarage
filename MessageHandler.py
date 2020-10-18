from GSMModemClass import GSMModem
from PDUClass import GSMMessage
from time import sleep
import logging
import sys
DOOR_CLOSED = 1

class smsmessagehandler:
  def __init__(self, initAttemps, Project):
    self.notification = False
    self.messagetreated = False
    self.projectboard = Project
    errcntr = 0
    logging.info("Initialisation of the modem in progress.")
    while errcntr < initAttemps:
      sleep(5)
      try:
        self.modem = GSMModem()
        logging.info("Modem initialisation SUCCESS.")
        self.ready = True
        break
      except:
        errcntr = errcntr + 1
        logging.error("Failed attempt [%i] to initialise the modem likely no access to ttyUSB0!" % errcntr)
        self.ready = False
  def ready(self):
    return True

  def sendmessage(self, destination, message):
    self.modem.sendMessage(destination,message)

  def treatsmsmessages(self):
    self.messagetreated = False
    msgNumbers = self.modem.getMessageNumbers()
    logging.debug("MessageNumbers in modem")
    logging.debug(msgNumbers)
    pulseSent = False
    for msgNr in msgNumbers:
      msg = self.modem.readMessage(msgNr)
      self.modem.deleteMessage(msgNr)
      if msg != "NOMSG":
        logging.debug("Decoding message retrieved from modem.")
        self.messagetreated = True
        try:
          readablemsg = GSMMessage(msg)
          logging.info("Message: %s " % readablemsg.getMessage())
          logging.info("Received from %s " % readablemsg.OANum)
          # Get a the next message from the SIM
          if readablemsg.OANum in ('+32471569200','+32471569201','+32471569206'):
            logging.info("Phone number %s is authorised to send requests" % readablemsg.OANum)
            smsmessage = readablemsg.getMessage()
            if "OPEN" in smsmessage.upper():
              if (pulseSent):
                logging.info("A pulse was already sent in this set of SMS's.")
                logging.info("Did 2 persons sent an Open command at the same time?")
              else:
                logging.info("Open pulse is now sent.")
                self.projectboard.sendpulse()
                pulseSent = True
            elif "CLOSE" in smsmessage.upper():
              if (pulseSent):
                logging.info("A pulse was already sent in this set of SMS's.")
                logging.info("Did 2 persons sent an Open command at the same time?")
              else:
                logging.info("Close pulse is now sent.")
                self.projectboard.sendpulse()
                pulseSent = True
            elif "STATUS" in smsmessage.upper():
              doorstatus = self.projectboard.getdoorstatus()
              # 1 indicates door is closed
              # 0 indicates door is open
              if doorstatus == DOOR_CLOSED:
                statusmessage = "STATUS : Door is CLOSED "
              else:
                statusmessage = "STATUS : Door is OPEN "
              if self.notification:
                statusmessage = statusmessage + " Notification ON "
              else:
                statusmessage = statusmessage + " Notification OFF "
              self.modem.sendMessage(readablemsg.OANum,statusmessage)
            elif "UNNOTIFY" in smsmessage.upper():
              logging.info("Notifications are turned OFF by SMS.")
              self.notification = False
            elif "NOTIFY" in smsmessage.upper():
              logging.info("Notifications are turned ON by SMS.")
              self.notification = True
            elif "HELP" in smsmessage.upper():
              logging.info("HELP Requested and sent to %s." % readablemsg.OANum)
              self.modem.sendMessage(readablemsg.OANum,"Commands are : STATUS , OPEN , UNNOTIFY , NOTIFY , HELP.")
            else:
              logging.warn("'%s' is not a valid command" % readablemsg.getMessage())
              if self.notification:
                self.modem.sendMessage(readablemsg.OANum,"INVALID COMMAND RECEIVED. Valid commands are : STATUS , OPEN , UNNOTIFY , NOTIFY , HELP.")
            smsmessage = ""
          else:
            logging.warn("Phone number %s is NOT authorised to send requests" % readablemsg.OANum)
            self.modem.sendMessage('+32471569206',"ALERT SMS received from unauthorized number %s." % readablemsg.OANum)
        except:
            logging.error("Unexpected error:", sys.exc_info()[0])            
