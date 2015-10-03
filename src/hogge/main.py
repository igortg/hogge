from configparser import ConfigParser
import os
import random

import irsdk

from hogge.racemonitor import RaceMonitor
from hogge.sessiondashboard import SessionDashboard
from hogge.xlsdashboardwriter import XlsDashboardWriter

HOGGE_CONFIG_FILENAME = os.path.expanduser(r"~\Documents\Hogge\hogge.ini")


def print_title():
    log("== Hogge - iRacing Session Lap Chronometer ==")
    print("\t{0}".format(random.choice(HOGGE_QUOTES)))
    print()


def main():
    print_title()
    ir = irsdk.IRSDK()

    if not os.path.isfile(HOGGE_CONFIG_FILENAME):
        raise RuntimeError("No config file found")
    parser = ConfigParser()
    config = parser.read(HOGGE_CONFIG_FILENAME)

    dashboard = SessionDashboard.create_default_dashboard()
    monitor = RaceMonitor(ir, dashboard)
    log("Waiting for iRacing...\n")
    monitor.wait_for_telemeter()
    log("Connected. Start Monitoring\n")
    # noinspection PyBroadException
    try:
        monitor.start()
    finally:
        output_dir = config.get("General", "output_dir")
        driver_name = config.get("General", "driver_name")
        xls_basename = "{0} - {1}.xlsx".format(dashboard.name, driver_name)
        xls_filepath = os.path.join(output_dir, xls_basename)
        if not os.path.isdir(os.path.dirname(xls_filepath)):
            os.mkdir(os.path.dirname(xls_filepath))
        log("Saving session at {0}\{1}\n".format(output_dir, xls_basename))
        writer = XlsDashboardWriter(xls_filepath)
        writer.write(dashboard)
        input("Press any key to continue...")


def log(msg):
    print("{0}\n".format(msg))


HOGGE_QUOTES = [
    "Rubbin, son, is racin'",
    "Cole, when you shift the gear and that little needle on the tach goes into the red and reads 9000 RPMs, " \
    "that's BAD.",
    "Well, I know a damn race driver when I see one."
]


if __name__ == '__main__':
    main()