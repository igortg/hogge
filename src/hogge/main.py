import os
import random

import irsdk

from hogge.racemonitor import RaceMonitor
from hogge.sessiontimesheet import SessionTimeSheet
from hogge.xlsdashboardwriter import XlsDashboardWriter


def print_title():
    log("== Hogge - iRacing Session Lap Chronometer ==")
    print("\t{0}".format(random.choice(HOGGE_QUOTES)))
    print()


HOGGE_DATA_DIR = r"~\Documents\Hogge Sessions"

def main():
    print_title()
    ir = irsdk.IRSDK()
    dashboard = SessionTimeSheet.create_default_timesheet()
    monitor = RaceMonitor(ir, dashboard)
    log("Waiting for iRacing...\n")
    monitor.wait_for_telemeter()
    log("Connected. Start Monitoring\n")
    # noinspection PyBroadException
    try:
        monitor.start()
    finally:
        xls_basename = "{0}.xlsx".format(dashboard.name)
        xls_filepath = os.path.join(os.path.expanduser(HOGGE_DATA_DIR), xls_basename)
        if not os.path.isdir(os.path.dirname(xls_filepath)):
            os.mkdir(os.path.dirname(xls_filepath))
        log("Saving session at {0}\{1}\n".format(HOGGE_DATA_DIR, xls_basename))
        writer = XlsDashboardWriter(xls_filepath)
        writer.write(dashboard)
        input("Press any key to continue...")


def log(msg):
    print("{0}\n".format(msg))


HOGGE_QUOTES = [
    "Rubbin, son, is racin'",
    "Cole, when you shift the gear and that little needle on the tach goes into the red and reads 9000 RPMs, that's BAD.",
    "Well, I know a damn race driver when I see one."
]


if __name__ == '__main__':
    main()