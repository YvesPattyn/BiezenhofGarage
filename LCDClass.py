#!/usr/bin/python

import smbus
import time
import datetime

I2C_ADDR  = 0x27 # I2C device address
LCD_WIDTH = 16   # Maximum characters per line

# Define some device constants
LCD_CHR = 1 # Mode - Sending data
LCD_CMD = 0 # Mode - Sending command

LCD_LINE_1 = 0x80 # LCD RAM address for the 1st line
LCD_LINE_2 = 0xC0 # LCD RAM address for the 2nd line

LCD_BACKLIGHT  = 0x08  # On 0X08 / Off 0x00

ENABLE = 0b00000100 # Enable bit

E_PULSE = 0.0005
E_DELAY = 0.0005

class lcd:
    name = ""
    gpiopin = 0

    def __init__(self):
      self.bus = smbus.SMBus(1) # Rev 2 Pi uses 1
      self.lcd_byte(0x33,LCD_CMD) # 110011 Initialise
      self.lcd_byte(0x32,LCD_CMD) # 110010 Initialise
      self.lcd_byte(0x06,LCD_CMD) # 000110 Cursor move direction
      self.lcd_byte(0x0C,LCD_CMD) # 001100 Display On,Cursor Off, Blink Off
      self.lcd_byte(0x28,LCD_CMD) # 101000 Data length, number of lines, font size
      self.lcd_byte(0x01,LCD_CMD) # 000001 Clear display
      time.sleep(E_DELAY)

    def lcd_byte(self,bits, mode):

      bits_high = mode | (bits & 0xF0) | LCD_BACKLIGHT
      bits_low = mode | ((bits<<4) & 0xF0) | LCD_BACKLIGHT

      self.bus.write_byte(I2C_ADDR, bits_high)
      self.lcd_toggle_enable(bits_high)

      self.bus.write_byte(I2C_ADDR, bits_low)
      self.lcd_toggle_enable(bits_low)

    def lcd_toggle_enable(self,bits):
      time.sleep(E_DELAY)
      self.bus.write_byte(I2C_ADDR, (bits | ENABLE))
      time.sleep(E_PULSE)
      self.bus.write_byte(I2C_ADDR,(bits & ~ENABLE))
      time.sleep(E_DELAY)

    def lcd_string(self,message,line):
      message = message.ljust(LCD_WIDTH," ")
      self.lcd_byte(line, LCD_CMD)
      for i in range(LCD_WIDTH):
          self.lcd_byte(ord(message[i]),LCD_CHR)

