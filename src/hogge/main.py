import os

import irsdk

from hogge.racemonitor import RaceMonitor
from hogge.xlssessiondashboard import XlsSessionDashboard


def main():
    log("")
    ir = irsdk.IRSDK()
    xls_filename = os.path.expanduser(r"~\Documents\hogge-session.xlsx")
    dashboard = XlsSessionDashboard.create_default_dashboard(xls_filename)
    monitor = RaceMonitor(ir, dashboard)
    log("Waiting for iRacing...\n")
    monitor.wait_for_telemeter()
    log("Connected. Start Monitoring\n")
    # noinspection PyBroadException
    try:
        monitor.start()
    finally:
        log("Saving session at {0}\n".format(xls_filename))
        dashboard.close_dashboard()
        input("Press any key to continue...")


def log(msg):
    print("{0}\n".format(msg))


if __name__ == '__main__':
    main()