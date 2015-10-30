from jinja2 import Environment, PackageLoader
import os
import math


class HtmlTimeSheetWriter(object):


    def __init__(self, basename, output_dir):
        self.basename = basename
        self._output_dir = output_dir
        self.env = Environment(loader=PackageLoader("hogge", "templates"))
        self.env.filters["laptime"] = self.float2laptime
        self.env.filters["fuel"] = lambda x: "{:.2f}".format(x)


    def dump(self, timesheet):
        """

        :param SessionTimeSheet timesheet: the time sheet to dump
        """
        out_filename = os.path.join(self._output_dir, "{}.html".format(self.basename))
        template = self.env.get_template("htmltimesheet.html")
        ostream = template.stream(timesheet=timesheet, summary=timesheet.create_summary())
        ostream.dump(out_filename)


    @staticmethod
    def float2laptime(value):

        def get_microseconds(value):
            return (value % math.floor(value)) * 1e3

        if value >= 60:
            return "{:.0f}:{:02.0f}.{:.0f}".format(value // 60, value % 60, get_microseconds(value))
        else:
            return "{:.0f}.{:.0f}".format(value, get_microseconds(value))
