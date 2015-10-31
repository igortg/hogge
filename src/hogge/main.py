from configparser import ConfigParser
import os
import random

import irsdk
from hogge.htmltimesheetwriter import HtmlTimeSheetWriter

from hogge.racemonitor import RaceMonitor
from hogge.sessiontimesheet import SessionTimeSheet
from hogge.xlsdashboardwriter import XlsDashboardWriter

HOGGE_CONFIG_FILENAME = os.path.expanduser(r"~\Documents\Hogge\hogge.ini")


def print_title():
    log("== Hogge - iRacing Session Lap Chronometer ==")
    print("\t{0}".format(random.choice(HOGGE_QUOTES)))
    print()


def main():
    print_title()

    if not os.path.isfile(HOGGE_CONFIG_FILENAME):
        raise RuntimeError("No config file found")
    config = ConfigParser()
    config.read(HOGGE_CONFIG_FILENAME)
    output_dir = config.get("General", "output_dir")
    driver_name = config.get("General", "driver_name")
    ir = irsdk.IRSDK()
    timesheet = SessionTimeSheet.create_default_timesheet()
    writer = HtmlTimeSheetWriter()

    def on_lap(lap_register):
        basename = os.path.join(output_dir, "{0} - {1}".format(timesheet.name, driver_name))
        log("Saving session at {}".format(basename))
        writer.dump(timesheet, basename)

    monitor = RaceMonitor(ir, timesheet, on_lap)
    log("Waiting for iRacing...")
    monitor.wait_for_telemeter()
    log("Connected. Start Monitoring")
    # noinspection PyBroadException
    try:
        monitor.start()
    finally:
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