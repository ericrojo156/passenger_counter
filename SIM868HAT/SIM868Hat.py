#!/usr/bin/python

'''
Author : Chris Todd
Organization: ECE499

'''
import serial
import traceback
import sys
import logging
import os
import socket
import time
import struct
import ctypes
import random
import binascii
import errno
import argparse as ap
from threading import Thread
from threading import Condition
from collections import OrderedDict

from logging.config import fileConfig
from datetime import datetime, timedelta

log = None
ss = None

LOG_LEVEL = 'DEBUG'           # Set log level: 'DEBUG','INFO'
SERIAL_PORT = '/dev/serial1'  # Location of serial port bound to AUX2
BAUDRATE = 115200               # Baud rate of serial connection
TERM_CHAR = '\n'               # Termination character ('<' Default)
START_CHAR = '>'              # Message must be delimited by START_CHAR

task_runtime_info = {}


def parseInt(intStr):
    try:
        if intStr == "":
            return 0
        else:
            return int(intStr)

    except ValueError as e:
        log.error('Unable to Parse Value: %s, %s' % (intStr, e.message))
    except Exception:
        PrintException(log)


def parseFloat(floatStr):
    try:
        if floatStr == "":
            return 0
        else:
            return float(floatStr)

    except ValueError as e:
        log.error('Unable to Parse Value: %s, %s' % (floatStr, e.message))
    except Exception:
        PrintException(log)


class UTCDateTime(object):

    def __init__(self, UTCStr=""):

        self._UTCStr = UTCStr
        self.year = 0
        self.month = 0
        self.day = 0
        self.hour = 0
        self.minute = 0
        self.second = 0
        self.fracSec = 0

        if len(UTCStr) > 0:
            self.parseUTCTimeData()

    def __str__(self):
        return "%04d-%02d-%02d %02d:%02d:%02d.%02d" % \
                (self.year, self.month, self.day,
                 self.hour, self.minute, self.second,
                 self.fracSec)

    def parseUTCTimeData(self):

        if isinstance(self._UTCStr, str):
            self._UTCStr = str(self._UTCStr)
        else:
            log.warn('GNSS Information NOT of type string...')
            return

        if len(self._UTCStr) != 18:
            log.error('Malformatted UTC Info String = %s', self._UTCStr)
            return

        try:
            self.year = int(self._UTCStr[0:4])
            self.month = int(self._UTCStr[4:6])
            self.day = int(self._UTCStr[6:8])
            self.hour = int(self._UTCStr[8:10])
            self.minute = int(self._UTCStr[10:12])
            self.second = int(self._UTCStr[12:14])
            self.fracSec = int(self._UTCStr[15:18])

        except ValueError as e:
            log.error('Unable to Parse Value: %s, %s' % (val, e.message))
        except Exception:
            PrintException(log)


class LocationData(object):

    def __init__(self, GNSInfoStr=""):

        self._GNSInfoStr = GNSInfoStr

        self.gnsOn = None
        self.gnsFix = None
        self.utcDateTime = UTCDateTime()
        self.lat = 0.0
        self.lon = 0.0
        self.alt = 0
        self.speed = 0.0
        self.course = 0.0
        self.fixMode = 0
        self.HDOP = 0.0
        self.PDOP = 0.0
        self.VDOP = 0.0
        self.nsatsGPS = 0
        self.nsatsGNSSUsed = 0
        self.nsatsGLONASS = 0
        self.cno = 0
        self.VPA = 0
        self.HPA = 0

        if len(self._GNSInfoStr) > 0:
            self.parseGNSSLocData()

    def __str__(self):
        prnStr = "--------------- GNSS INFO ----------------\n"
        prnStr += "%15s = %r\n" % ("gnsOn", self.gnsOn)
        prnStr += "%15s = %r\n" % ("gnsFix", self.gnsFix)
        prnStr += "%15s = %s\n" % ("UTC Date Time", self.utcDateTime)
        prnStr += "%15s = %f\n" % ("Latitude", self.lat)
        prnStr += "%15s = %s\n" % ("Longitude", self.lon)
        prnStr += "%15s = %f\n" % ("Altitude", self.alt)
        prnStr += "%15s = %f\n" % ("Speed", self.speed)
        prnStr += "%15s = %f\n" % ("Course", self.course)
        prnStr += "%15s = %d\n" % ("Fix Mode", self.fixMode)
        prnStr += "%15s = %f\n" % ("HDOP", self.HDOP)
        prnStr += "%15s = %f\n" % ("PDOP", self.PDOP)
        prnStr += "%15s = %f\n" % ("VDOP", self.VDOP)
        prnStr += "%15s = %d\n" % ("GPS Satellites", self.nsatsGPS)
        prnStr += "%15s = %d\n" % ("GNSS Satellites Used", self.nsatsGNSSUsed)
        prnStr += "%15s = %d\n" % ("GLONASS Satellites", self.nsatsGLONASS)
        prnStr += "%15s = %d\n" % ("c/no", self.cno)
        prnStr += "%15s = %f\n" % ("VPA", self.VPA)
        prnStr += "%15s = %f\n" % ("HPA", self.HPA)

        return prnStr

    def parseGNSSLocData(self):

        if isinstance(self._GNSInfoStr, str):
            self._GNSInfoStr = str(self._GNSInfoStr)
        else:
            log.warn('GNSS Information NOT of type string...')
            return

        data = self._GNSInfoStr.split(':')

        if len(data) >= 2:
            data = data[1]
        else:
            log.error('Data String Not Found')
            return

        field = data.split(',')

        if len(field) != 21:
            log.error('Malformatted GNSS Info String = %s', self._GNSInfoStr)
            return

        self.gnsOn = parseInt(field[0])
        self.gnsFix = parseInt(field[1])
        self.utcDateTime = UTCDateTime(field[2])
        self.lat = parseFloat(field[3])
        self.lon = parseFloat(field[4])
        self.alt = parseFloat(field[5])
        self.speed = parseFloat(field[6])
        self.course = parseFloat(field[7])
        self.fixMode = parseInt(field[8])
        # Field[9] Reserved
        self.HDOP = parseFloat(field[10])
        self.PDOP = parseFloat(field[11])
        self.VDOP = parseFloat(field[12])
        # Field[13] Reserved
        self.nsatsGPS = parseInt(field[14])
        self.nsatsGNSSUsed = parseInt(field[15])
        self.nsatsGLONASS = parseInt(field[16])
        # Field[17] Reserved
        self.cno = parseInt(field[18])
        self.HPA = parseFloat(field[19])
        self.VPA = parseFloat(field[20])


class SIM868Module(serial.Serial):

    def __init__(self, port, baudrate):

        self._keepRunning = True
        self._expect = ""
        self._ATResp = ""
        self.loc = LocationData()

        while True:
            try:
                super(SIM868Module, self).__init__(port, baudrate)
                self.write_timeout = 0  # Non-Blocking
                break
            except serial.SerialException:
                log.fatal('SerialException While Opening Serial Port')
                PrintException(log)
                time.sleep(5)
                continue
            except Exception:
                log.fatal('FATAL: Exception While Opening Serial Port')
                time.sleep(5)
                continue

        self._rcvThread = Thread(target=self.handleATResponse, args=())
        self._rcvThread.daemon = True
        self._rcvCondition = Condition()
        self._rcvThread.start()

    def handleATResponse(self):

        while self._keepRunning:
            msg = self.read_until()  # Default is carriage return

            msgStr = ""

            if isinstance(msg, str):
                msgStr = msg

            msgStr = msgStr.replace("\r\n", "")

            if msgStr is not "":
                log.info('<< %s' % msgStr)
                if self._expect is not "" and msgStr == self._expect:
                    self._rcvCondition.acquire()
                    self._ATResp = msgStr
                    self._rcvCondition.notify()
                    self._rcvCondition.release()

                if msgStr.startswith("+CGNSINF"):
                    self.loc = LocationData(msgStr)

    def sendATCmd(self, cmd, expect=None, footer="\r\n"):

        if expect is not None:
            self._expect = expect

        cmdStr = ""

        if isinstance(cmd, str):
            cmdStr = cmd
        else:
            return -1

        if not cmdStr.endswith("\r\n"):
            cmdStr += "\r\n"

        self.write(cmdStr)
        if expect is not None:
            self._rcvCondition.acquire()
            self._rcvCondition.wait(2.0)
            self._rcvCondition.release()

            if expect == self._ATResp:
                log.info("Received Desired AT Response")
            else:
                log.info("TIMEOUT Waiting for Response")

        self._expect = ""


def logInit():

    logConfigFile = os.path.join(os.path.dirname(
        os.path.realpath(__file__)), 'logging.ini')
    try:
        fileConfig(logConfigFile)
    except IOError as error:
        print 'Failed loading log config file: %s' % error
        if error.errno == errno.EROFS:
            logger = logging.getLogger()
            ch = logging.StreamHandler()
            ch.setLevel(logging.DEBUG)
            logger.addHandler(ch)


def PrintException(log):
    """
    Print an exception nicely to the log.

    Args:
        log (logger): logger used by the task from
        which this exception was thrown
    """
    _, exc_obj, tb = sys.exc_info()
    lastTrace = traceback.extract_tb(tb)[-1]
    filename = lastTrace[0]
    lineno = lastTrace[1]
    line = lastTrace[3]

    if log is not None:
        if log.name in task_runtime_info:
            task_runtime_info[log.name]['last_exception_thrown'] = {
                'file': filename,
                'line': lineno,
                'msg': str(exc_obj)
            }
        log.error('EXCEPTION IN ({}:{} "{}"): {}'.format(
            filename, lineno, line.strip(), exc_obj))
    else:
        print('EXCEPTION IN ({}:{} "{}"): {}'.format(
            filename, lineno, line.strip(), exc_obj))


if __name__ == "__main__":

    logInit()
    log = logging.getLogger("console")
    log.setLevel(LOG_LEVEL)

    try:
        ss = SIM868Module("/dev/ttyUSB2", 115200)
        ss.sendATCmd("ATE0")
        ss.sendATCmd("AT", "OK")

        while True:
            ss.sendATCmd("AT+CGNSINF")
            time.sleep(0.5)
            print(ss.loc)
            time.sleep(0.5)

    except KeyboardInterrupt:
        log.warn('KeyBoardInterrupt, Exiting SIM868')
    except Exception:
        PrintException(log)
    finally:
        if ss is not None:
            log.info('Closing Serial Port')
            ss._keepRunning = False
            ss.close()
            sys.exit(0)
