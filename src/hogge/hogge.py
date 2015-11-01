from configparser import ConfigParser
import configparser
import os
import random
from string import Template

import irsdk
from hogge.htmltimesheetwriter import HtmlTimeSheetWriter

from hogge.racemonitor import RaceMonitor
from hogge.sessiontimesheet import SessionTimeSheet
from hogge.xlsdashboardwriter import XlsDashboardWriter


class Hogge(object):

    HOGGE_DATA_DIRNAME = os.path.expanduser(r"~\Documents\Hogge")


    def __init__(self):
        if not os.path.isdir(self.HOGGE_DATA_DIRNAME):
            os.mkdir(self.HOGGE_DATA_DIRNAME)
        config = self._acquire_config_data()
        self.output_dir = config.get("General", "output_dir")
        ir = irsdk.IRSDK()
        self._monitor = RaceMonitor(ir, self.on_lap_completed)
        self._writer = HtmlTimeSheetWriter()
        self._active_timesheet = None


    def main(self):
        monitor = self._monitor
        while True:
            self._active_timesheet = SessionTimeSheet.create_default_timesheet()
            log("Waiting for iRacing...  (use Ctrl+C to interrupt)")
            monitor.wait_for_telemeter()
            log("Connected. Start Monitoring")
            monitor.start()
        input("Press any key to continue...")


    def on_lap_completed(self, lap_register):
        timesheet = self._active_timesheet
        if not timesheet.name:
            timesheet.name = self._monitor.get_session_name()
        sheet_filename = os.path.join(self.output_dir, "{0}.html".format(timesheet.name))
        if not os.path.isfile(sheet_filename):
            log("Saving session at {}".format(sheet_filename))
        self._writer.dump(timesheet, sheet_filename)


    def _acquire_config_data(self):
        config_filename = os.path.join(self.HOGGE_DATA_DIRNAME, "hogge.ini")
        if not os.path.isfile(config_filename):
            with open(config_filename, "w") as config_file:
                tpl = Template(CONFIG_TEMPLATE)
                config_file.write(tpl.substitute(output_dir=self.HOGGE_DATA_DIRNAME))
        config = configparser.ConfigParser()
        config.read(config_filename)
        return config


def log(msg):
    print("{0}\n".format(msg))


CONFIG_TEMPLATE = """[General]
output_dir = $output_dir
"""


HOGGE_QUOTES = [
    "Rubbin, son, is racin'",

    "Cole, when you shift the gear and that little needle on the tach goes into the red and reads 9000 RPMs, " \
    "that's BAD!",

    "Well, I know a damn race driver when I see one.",

    "I want you to back out on the track and hit the pace car!",
]