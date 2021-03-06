import os
from jinja2 import Environment, FileSystemLoader
import math


class HtmlTimeSheetWriter(object):


    def __init__(self):
        self._env = Environment(loader=FileSystemLoader(os.path.join(get_exe_dirname(), "templates")))
        self._env.filters["laptime"] = self.float2laptime
        self._env.filters["fuel"] = lambda x: "{:.2f}".format(x)
        self.template = self._env.get_template("htmltimesheet.html")


    def dump(self, timesheet, output_filename):
        """
        Write the timeheet into a file.

        :param SessionTimeSheet timesheet: the time sheet to dump

        :param str output_filename: timesheet file to be created
        """
        ostream = self.template.stream(timesheet=timesheet, summary=timesheet.create_summary())
        ostream.dump(output_filename)


    @staticmethod
    def float2laptime(value):

        def get_microseconds(time_value):
            if time_value > 0:
                return (time_value % math.floor(time_value)) * 1e3
            else:
                return 0

        if value >= 60:
            return "{:.0f}:{:02.0f}.{:03.0f}".format(value // 60, math.floor(value % 60), get_microseconds(value))
        else:
            return "{:.0f}.{:.0f}".format(value, get_microseconds(value))


def get_exe_dirname():
    import sys
    if hasattr(sys, "frozen"):
        return os.path.dirname(sys.executable)
    else:
        import hogge
        return os.path.join(os.path.dirname(hogge.__file__), "../dist")