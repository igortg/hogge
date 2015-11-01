from jinja2 import Environment, PackageLoader
import math


class HtmlTimeSheetWriter(object):


    def __init__(self):
        self.env = Environment(loader=PackageLoader("hogge", "templates"))
        self.env.filters["laptime"] = self.float2laptime
        self.env.filters["fuel"] = lambda x: "{:.2f}".format(x)


    def dump(self, timesheet, output_filename):
        """
        Write the timeheet into a file.

        :param SessionTimeSheet timesheet: the time sheet to dump

        :param str output_filename: timesheet file to be created
        """
        template = self.env.get_template("htmltimesheet.html")
        ostream = template.stream(timesheet=timesheet, summary=timesheet.create_summary())
        ostream.dump(output_filename)


    @staticmethod
    def float2laptime(value):

        def get_microseconds(time_value):
            if time_value > 0:
                return (time_value % math.floor(time_value)) * 1e3
            else:
                return 0

        if value >= 60:
            return "{:.0f}:{:02.0f}.{:03.0f}".format(value // 60, value % 60, get_microseconds(value))
        else:
            return "{:.0f}.{:.0f}".format(value, get_microseconds(value))
