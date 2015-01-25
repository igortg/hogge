import os

import irsdk

from hogge.racemonitor import RaceMonitor
from hogge.sessiondashboard import SessionDashboard
from hogge.xlsdashboardwriter import XlsDashboardWriter


def print_title():
    log("== Hogge - iRacing Session Lap Telemetry ==")
    print("\t{0}".format(HOGGE_QUOTES[0]))
    print("                   Hogge, Harry")
    print()


HOGGE_DATA_DIR = r"~\Documents\Hogge Sessions"

def main():
    print_title()
    ir = irsdk.IRSDK()
    dashboard = SessionDashboard.create_default_dashboard()
    monitor = RaceMonitor(ir, dashboard)
    log("Waiting for iRacing...\n")
    monitor.wait_for_telemeter()
    log("Connected. Start Monitoring\n")
    # noinspection PyBroadException
    try:
        monitor.start()
    finally:
        if not os.path.isdir(HOGGE_DATA_DIR):
            os.mkdir(HOGGE_DATA_DIR)
        xls_basename = "{0}.xlsx".format(dashboard.name)
        xls_filepath = os.path.join(os.path.expanduser(HOGGE_DATA_DIR), xls_basename)
        log("Saving session at {0}\{1}\n".format(HOGGE_DATA_DIR, xls_basename))
        writer = XlsDashboardWriter(xls_filepath)
        writer.write(dashboard)
        input("Press any key to continue...")


def log(msg):
    print("{0}\n".format(msg))


HOGGE_QUOTES = [
    "Rubbin, son, is racin'",
    "Cole, when you shift the gear and that little needle on the tach goes into the red and reads 9000 RPMs, that's BAD.",
]


if __name__ == '__main__':
    main()