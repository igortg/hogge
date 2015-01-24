from collections import namedtuple
import xlsxwriter


DashboardColumn = namedtuple("Dashboard", ["measure_id", "title", "type"])

class SessionDashboard(object):

    def __init__(self, excel_filename):
        self._workbook = xlsxwriter.Workbook(excel_filename)
        self._worksheet = self._workbook.add_worksheet()
        self._columns = []
        self._laps = []


    def add_column(self, *kwargs):
        self._columns.append(DashboardColumn(*kwargs))


    def save_lap(self, lap_register):
        if not self._laps:
            self._write_header()
        self._laps.append(lap_register)
        self._write_lap(lap_register)


    def _write_header(self):
        for i, column in enumerate(self._columns):
            self._worksheet.write(0, i, column.title)


    def _write_lap(self, lap_register):
        # row = []
        # for measure_id, _, typecode in self._columns:
        #     measure_text = self._to_string(lap_register[measure_id], typecode)
        #     row.append(measure_text)
        # self._stream.write("\t".join([text for text in row]))
        # self._stream.write(ENDLINE)


    def _to_string(self, param, typecode):
        if typecode == "time":
            return strftime(param)
        else:
            return str(param)

def strftime(seconds):
    return "{0:.0f}:{1:.3f}".format(seconds // 60, seconds % 60)


ENDLINE = "\n"