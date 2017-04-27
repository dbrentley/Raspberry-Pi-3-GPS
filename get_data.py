#!/usr/bin/env python3

from gps.gps_class import GPS
import time
import sys

def main():
    gps_data = GPS(device='/dev/ttyS0')
    print("Press Control-C to stop.")
    gps_data.start()

    try:
        while True:
            print("{}, lat: {}, lon: {}, elevation: {}ft, speed: {}mph".format(
                gps_data.local_time,
                gps_data.lat,
                gps_data.lon,
                gps_data.altitude,
                gps_data.mph))
            time.sleep(1)
    except KeyboardInterrupt:
        gps_data.stop()
        sys.exit(0)

if __name__ == '__main__':
    main()
