#!/usr/bin/python3
'''
Created on May 15, 2019

@author: ctodd
'''
import argparse as ap
import ctypes
import binascii
import time
import struct
import unittest
import random
import socket
from HaInterface import pmr
from datetime import datetime, timedelta
LOCAL_PORT = 2001

pmrmod = None

def sendAPC():
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    while True:
        pmrmod.readStatus()

        currTime = datetime.utcnow()
        posStr = ",%0.5f,%0.5f," % (pmrmod.lat, pmrmod.lon)
        dateStr = currTime.strftime("%m%d%Y,%H%M%S")
        course = ",%d,%d," % (pmrmod.heading, pmrmod.speed)

        apc = '>T,001,111016,63,06,00,00,116,176,000,000,116,176,000,000,03039F,16503<'
        apc_record = apc + posStr + dateStr + course + ",UTC"

        apc_record = apc_record.encode('utf-8')
        
        
        print('Msg Contents:\n[%s]' % binascii.hexlify(apc_record))

        

        try:
            sock.sendto(apc_record, ("24.68.124.121", LOCAL_PORT))
        except socket.error as e:
            log.error('Error Sending Parameter Write to localhost:%d...%s'
                    % (LOCAL_PORT, e.message))
        except Exception as e:
            print("Unknown Exception Sending Parameter Message on localhost 20510")
            print(e)

        time.sleep(1.0)


if __name__ == "__main__":
    try:
        pmrmod = pmr.HostedApp()
        sendAPC()
    except KeyboardInterrupt:
        if pmrmod is not None:
            pmrmod._deregister()
    
    
