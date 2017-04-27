import os
import time
import math
import serial
import threading
from datetime import datetime

class GPS:
    """
    GPS information: http://aprs.gids.nl/nmea/

    Raspberry Pi3 Model B with Gowoops GPS Module U-blox NEO-6M
    https://www.amazon.com/gp/product/B01AW5QYES

    @author: Brent Douglas
    """

    data = {}
    zones = {}
    running = False
    device = None
    thread = None

    utc_time = 0
    local_time = None
    lat_raw = 0
    lat = 0
    lat_d = None
    lon_raw = 0
    lon = 0
    lon_d = None
    quality = 0
    sats = 0
    dilution_h = 0
    altitude = 0
    units = None
    separation = 0
    separation_u = None
    age = 0
    station = 0
    kph = 0
    mph = 0

    def __init__(self, device):
        os.nice(19)
        self.device = device
        self.data = { 'gpgga': self.gpgga, 'gpvtg': self.gpvtg }

    def start(self):
        self.running = True
        self.thread = threading.Thread(target=self.main_thread)
        self.thread.start()

    def stop(self):
        self.running = False
        self.thread.join()

    def main_thread(self):
        with serial.Serial(self.device, 9600, timeout=1) as ser:
            while self.running:
                line = ser.readline()
                r = line.decode('utf-8').split(',')
                r[-1] = r[-1].replace('\r\n', '')
                try:
                    self.data[r[0].replace('$', '').lower()](r[1:])
                except:
                    pass

    def gpgga(self, d):
        # Global Positioning System Fix Data
        self.utc_time = d[0] # hhmmss.ss = UTC of position
        self.lat_raw = d[1] # llll.ll = Latitude of position
        self.lat_d = d[2] # a = N or S
        self.lon_raw = d[3] # yyyyy.yy = Longitude of position
        self.lon_d = d[4] # a = E or W
        self.quality = d[5] # GPS quality (0=no fix, 1=GPS fix, 2=Dif. GPS fix)
        self.sats = d[6] # xx = Number of satellites in use
        self.dilution_h = d[7] # x.x = Horizontal dilution of precision
        self.altitude = self.meters_to_feet(d[8]) # x.x = Antenna altitude above mean-sea-level
        self.units = d[9] # M = Units of antenna altitude, meters
        self.separation = d[10] # x.x = Geoidal separation
        self.separation_u = d[11] # M = Units of geoidal separation, meters
        self.age = d[12] # x.x = Age of differential GPS data (seconds)
        self.station = d[13] # xxxx = Differential reference station ID

        self.lat = "{0:.6f}".format(float(self.lat_raw[:2]) + (float(self.lat_raw[2:]) / 60))
        self.lon = "-{0:.6f}".format(float(self.lon_raw[:3]) + (float(self.lon_raw[3:]) / 60))

        self.local_time = self.utc_to_local(self.utc_time)

    def gpvtg(self, d):
        self.kph = d[6]
        self.mph = self.kph_to_mph(self.kph)

    def meters_to_feet(self, m):
        return "{}".format(round(float(m) * 3.28084))
        #return "{0:.1f}".format(float(m) * 3.28084)

    def kph_to_mph(self, kph):
        return kph * 0.621371

    def utc_to_local(self, utc):
        # TODO: do some real offset stuff
        hh = (int(utc[:2]) - 7)
        mm = utc[2:4]
        ss = utc[4:6]
        if hh > 12:
            hh -= 12
            ampm = "p"
        else:
            ampm = "a"
        return "{}:{}:{}{}".format(hh, mm, ss, ampm)
