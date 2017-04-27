#!/usr/bin/env python3

from gps.gps_class import GPS
import time

def main():
    gps_data = GPS('/dev/ttyS0')
    gps_data.start()

    while True:
        print("lat: {}, lon: {}, elevation: {}ft, speed: {}mph".format(
            gps_data.lat, gps_data.lon, gps_data.altitude, gps_data.mph))
        time.sleep(1)

if __name__ == '__main__':
    main()
