from bitstring import Bits
from bitstring import ConstBitStream
import logging

class GSMMessage:

  def __init__(self,HexMessage):
    logging.basicConfig(level=logging.INFO)
    logging.debug('-------Instantiate GSMMessage --------')
    self.fullStream = ConstBitStream('0x' + HexMessage)
    #Service Centre Address
    #######################

    # Read SCA Length [1]
    self.SCALen = self.fullStream.read('int:8') - 1

    # Read Type [1]
    self.SCATyp = self.fullStream.read('hex:8')

    # Read Address [SCALen x 8]
    temp = self.fullStream.read('hex:%i' % (self.SCALen *8) )

    # Format to readable phone number
    result= ""
    for x in range(1,len(temp),2):
      result = result + temp[x] + temp[x-1]
    self.SCANum = "+" + result[:result.find('f')]

    #PDU Type [1]
    self.PDUTyp = self.fullStream.read('bin:8')
    self.Multipart = self.PDUTyp[1:2]

    #Origination Address
    ####################

    # Read Length [1]
    self.OALen = self.fullStream.read('int:8') - 5

    # Read Type [1]
    self.OATyp = self.fullStream.read('hex:8')

    # Read Address [OALen x8]
    temp = self.fullStream.read('hex:%i' % (self.OALen *8) )

    # Format to readable phone number
    result= ""
    for x in range(1,len(temp),2):
      result = result + temp[x] + temp[x-1]
    self.OANum = "+" + result[:result.find('f')]

    #PDU PID [1]
    self.PID = self.fullStream.read('hex:8')

    #PDU DCS [1]
    self.DCS = self.fullStream.read('hex:8')

    #Timestamp
    ##########
    temp = self.fullStream.read('hex:56')
    # Format Timestamp
    result= ""
    for x in range(1,len(temp),2):
      result = result + temp[x] + temp[x-1]
    self.SCTS = "20" + result
    #User Data
    ##########

    #User Data Length
    self.UDL = self.fullStream.read('uint:8')
    #User Data Header if Multipart
    if (self.Multipart == '1'):
      self.UDHL = self.fullStream.read('int:8')
      self.UDH = self.fullStream.read('hex:40')
      self.UDH_Type = self.UDH[0:2]
      self.UDH_Len = self.UDH[2:4]
      self.UDH_ID = self.UDH[4:6]
      self.UDH_MsgNr = self.UDH[6:8]
      self.UDH_NbrMsgs = self.UDH[8:10]
    else:
      self.UDHL = 0
      self.UDH = ''
    #Calculate number of bits to read, make sure to read full 8 bytes.
    if ( (self.UDL % 8)!=0 ):
      bitsToRead = (self.UDL * 7) + ( 8 - (self.UDL * 7) % 8 )
    else:
      bitsToRead = self.UDL * 7
    if (self.UDHL != 0):
      bitsToRead = bitsToRead - ( 8 * (self.UDHL+1))
    logging.debug("PDU bitsToRead = %i" % bitsToRead)
    temp = self.fullStream.read('hex:%i' % bitsToRead )
    #Read User Data
    logging.debug("PDU Bytes = %s" % temp)
    #Format User Data and reverse order.
    result=''
    for x in range(0,len(temp),2):
      result = temp[x] + temp[x+1] + result
    logging.debug("PDU Reversed Bytes = %s" % result)
    self.UD = ConstBitStream('0x' + result)
    #Make a Bits format string in UDbin
    logging.debug("PDU len(result) = %i" % len(result) )
    self.UDbinL = len(result) * 4
    self.UDbin = self.UD.read('bin:%i' % (self.UDbinL ))
    logging.debug("PDU UDBin = %s" % self.UDbin)
    #print('Failed to decode UD')
    #self.UDbin = '0000'
    #self.UD = 'Error'
    self.PadBits = (self.UDL % 8) % 8

  def getMessage(self):
    # We need to shift a number of bits
    temp = self.UDbin[self.PadBits:]
    Message = ''
    for x in range(0,len(self.UDbin),7):
      b = temp[x:x+7]
      t = Bits(bin='0'+b)
      logging.debug('Bits:%s = [%s]' % (t,chr(t.int)))
      Message = chr(t.int) + Message
    return Message

  def getDate(self):
    t = self.SCTS
    return t[6:8] + "-" + t[4:6] + "-" + t[0:4]

  def getTime(self):
    t = self.SCTS
    return t[8:10] + ":" + t[10:12] + ":" + t[12:14]

  def dumpData(self):
    logging.info('SCALen    : %i' % self.SCALen)
    logging.info('SCATyp    : %s' % self.SCATyp)
    logging.info('SCANum    : %s' % self.SCANum)
    logging.info('PDUTyp    : %s' % self.PDUTyp)
    logging.info('OALen     : %i' % self.OALen)
    logging.info('OATyo     : %s' % self.OATyp)
    logging.critical('OANum     : %s' % self.OANum)
    logging.info('PID       : %s' % self.PID)
    logging.info('DCS       : %s' % self.DCS)
    logging.info('SCTS      : %s' % self.SCTS)
    logging.info('UDHL      : %i' % self.UDHL)
    if (self.UDHL > 0):
      logging.info('- UDH_Type   : %s' % self.UDH_Type)
      logging.info('- UDH_Len    : %s' % self.UDH_Len)
      logging.info('- UDH_ID     : %s' % self.UDH_ID)
      logging.info('- UDH_MsgNr  : %s' % self.UDH_MsgNr)
      logging.info('- UDH_NbrMsgs: %s' % self.UDH_NbrMsgs)
    logging.info('UDH       : %s' % self.UDH)
    logging.info('UDL       : %i' % self.UDL)
    logging.info('UD        : %s' % self.UD)
    logging.info('UDbin     : %s' % self.UDbin)
    logging.info('UDbinL    : %i' % self.UDbinL)
    logging.info('UDbinChars: %s' % str(len(self.UDbin)/7))
    logging.critical('Date      : %s' % self.getDate())
    logging.critical('Time      : %s' % self.getTime())
    logging.info('PadBits   : %i' % self.PadBits)
    logging.critical('Message   : %s' % self.getMessage())
    logging.info('Multipart : %s' % self.Multipart)
    
  def dumpShort(self):
    logging.info('----')
    logging.info(' Message : %s' % self.getMessage())
    logging.info(' Received on %s %s' % (self.getDate(),self.getTime()) )
    logging.info(' From %s' % self.OANum)
    logging.info('----')
