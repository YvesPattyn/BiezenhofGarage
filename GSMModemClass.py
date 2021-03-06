import serial
from curses import ascii
import logging

class GSMModem:
    def __init__(self):
        logging.info('Instance of GSMModem created.')
        self.ser = serial.Serial(port="/dev/ttyUSB0",baudrate=460800,timeout=1)
        # ATtention - Set Echo Off
        logging.debug(self.serialCommand("ATE0\r\n"))
        # Preferred Message Storage
        logging.info("Setting Preferred Message Storage - CPMS='SM','SM','SM'.")
        cmd = 'AT+CPMS="SM","SM","SM"\r\n'
        logging.debug(cmd)
        logging.debug(self.serialCommand(cmd))
        logging.info("Set text mode parameters for AT+CMGR commands.")
        cmd = "AT+CSDH=1\r\n"
        logging.debug(cmd)
        logging.debug(self.serialCommand(cmd))
        logging.info("Setting New Messages Intercept - CNMI=2,0,0,2,1")
        cmd = "AT+CNMI=2,0,0,2,1\r\n"
        logging.debug(cmd)
        logging.debug(self.serialCommand(cmd))
        # Check if PIN must be entered.
        logging.info("Checking PIN status.")
        cmd = "AT+CPIN?\r\n"
        logging.debug(cmd)
        pinCheck = self.serialCommand(cmd)
        if ( ("+CPIN" in pinCheck) and ("READY" in pinCheck) ):
          logging.info("PIN is still active. No need to enter it.")
        else:
          logging.info("PIN code is Required - Entering it now.")
          # Enter PIN code if required
          cmd = 'AT+CPIN="6089"\r\n'
          logging.debug(self.serialCommand(cmd))

    def serialCommand(self, cmd, message = ""):
        logging.debug("Serial Command %s Message <%s>" % (cmd.replace("\r\n",""),message))
        retval = ""
        if (message != ""):
          message = message + ascii.ctrl('Z')
          self.ser.write(cmd.encode())
          self.ser.write(message.encode())
        else:
          self.ser.write(cmd.encode())
        try:
          line = self.ser.readline()
          while ( line != b'' ):
            retval = retval + line.decode()
            logging.debug(line)
            line = self.ser.readline()
        except:
          retval = ""
        return retval

    def setMessageStore(self):
        # Preferred Message Storage
        logging.info("Setting Preferred Message Storage to SIM card CPMS='SM','SM','SM'.")
        cmd = 'AT+CPMS="SM","SM","SM"\r\n'
        logging.debug(cmd)
        logging.debug(self.serialCommand(cmd))

    def getAllMessages(self):
        # Text Mode on
        logging.debug("getAllMessages")
        logging.debug("Switching to TEXT mode.")
        cmd = "AT+CMGF=1\r\n"
        logging.debug(self.serialCommand(cmd))
        # List all messages
        cmd = 'AT+CMGL="ALL"\r\n'
        allMessages = self.serialCommand(cmd)
        logging.debug("--- allMessages ---- Begin")
        logging.debug(allMessages)
        logging.debug("--- allMessages ---- END")
        return allMessages

    def getMessageNumbers(self):
        logging.debug("getMessageNumbers")
        messageNumbers = [0]
        messageNumbers.clear()
        msgs = self.getAllMessages()
        splitted = msgs.split('\r\n')
        for x in splitted:
            if ("+CMGL:" in x):
                part1 = x.split(',')[0]
                messageNumbers.append(int(part1.replace('+CMGL: ','')))
        return messageNumbers

    def deleteMessage(self,messageNumber):
        logging.info("deleteMessage %s" % messageNumber)
        cmd ='AT+CMGD=%s\r\n' % messageNumber
        logging.debug(self.serialCommand(cmd))

    def deleteAllMessages(self):
        logging.info("deleteAllMessages")
        cmd ='AT+CMGD=1,4\r\n'
        logging.debug(self.serialCommand(cmd))

    def readMessage(self,messageNumber):
        logging.info("readMessage %s" % messageNumber)
        # PDU Mode on
        retval = "NOMSG"
        logging.debug("Switching to PDU mode.")
        cmd = "AT+CMGF=0\r\n"
        self.serialCommand(cmd)
        # Read message nr
        cmd ='AT+CMGR=%s\r\n' % messageNumber
        self.ser.write(cmd.encode())
        line = self.ser.readline()
        strLine = line.decode()
        logging.debug('Line before While = %s ' % strLine)
        while ( (strLine != '') and (line != b'\x00') ):
            logging.debug(strLine)
            if('0791' in strLine):
                logging.info('Line holding the message was found')
                retval = strLine
            line = self.ser.readline()
            strLine = line.decode()
        logging.info('ReadMessage returns = %s ' % retval)
        return retval

    def sendMessage(self,phoneNr,textMessage):
        logging.info("Sending Message %s to %s " % (textMessage, phoneNr))
        logging.debug("Switching to TEXT mode.")
        cmd = "AT+CMGF=1\r\n"
        self.ser.write(cmd.encode())
        textMessage = textMessage + ascii.ctrl('Z')
        cmd ='AT+CMGS="%s"\r\n' % phoneNr
        logging.debug(cmd)
        self.ser.write(cmd.encode())
        logging.debug(textMessage)
        self.ser.write(textMessage.encode())
        line = self.ser.readline()
        strLine = line.decode()
        logging.debug('Line before While = %s ' % strLine)
        while ( (strLine != '') and (line != b'\x00') ):
            line = self.ser.readline()
            strLine = line.decode()
            logging.debug(strLine)

    def getSettings(self):
        #cmd = 'AT+CPMS="SM","SM","SM"\r\n'
        #logging.info("SEND: Setting Prefered Message Store %s" % cmd.replace("\r\n",""))
        #retval = self.serialCommand(cmd)
        #logging.info("RECV: %s" % retval.replace("\r\n"," § "))

        # PIN Status
        cmd = "AT+CPIN?\r\n"
        logging.info("SEND: Query PIN status %s" % cmd.replace("\r\n",""))
        retval = self.serialCommand(cmd)
        logging.info("RECV: %s" % retval.replace("\r\n"," § "))

        # New Messages Intercept
        cmd = "AT+CNMI?\r\n"
        logging.info("SEND: Query New Message Intercept %s" % cmd.replace("\r\n",""))
        retval = self.serialCommand(cmd)
        logging.info("RECV: %s" % retval.replace("\r\n"," § "))
        if not "2,0,0,2,1" in retval:
            cmd = "AT+CNMI=2,0,0,2,1\r\n"
            logging.info("SEND: RESET New Message Intercept %s" % cmd.replace("\r\n",""))
            retval = self.serialCommand(cmd)
            logging.info("RECV: %s" % retval.replace("\r\n"," § "))

        # PDU status [1=Active]")
        cmd = "AT+CMGF?\r\n"
        logging.info("SEND: Query PDU status %s" % cmd.replace("\r\n",""))
        retval = self.serialCommand(cmd)
        logging.info("RECV: %s" % retval.replace("\r\n"," § "))

        # Preffered Message Storage"
        cmd = "AT+CPMS?\r\n"
        logging.info("SEND: Query Prefered Message Storage %s" % cmd.replace("\r\n",""))
        retval = self.serialCommand(cmd)
        logging.info("RECV: %s" % retval.replace("\r\n"," § "))

    def getStatus(self):
        cmd = "AT+CPMS?\r\n"
        logging.debug(cmd)
        retval = self.serialCommand(cmd)
        isOk = (retval.count('"SM"') == 3)
        if not isOk:
            logging.warning('Preffered Message Storage status is %s , while expecting "SM"' % retval)
            logging.warning('Attempting to reset to "SM","SM","SM" .')
            self.setMessageStore()
        return isOk

