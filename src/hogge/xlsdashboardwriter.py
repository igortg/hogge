import xlsxwriter
from hogge.sessiondashboard import SessionDashboard


class XlsDashboardWriter(object):


    def __init__(self, xls_filename):
        self._workbook = xlsxwriter.Workbook(xls_filename)
        self._worksheet = self._workbook.add_worksheet()
        self._type_formats = {
            SessionDashboard.DT_INT: self._workbook.add_format({"num_format": "0"}),
            SessionDashboard.DT_FLOAT: self._workbook.add_format({"num_format": "0.00"}),
            SessionDashboard.DT_LAP_TIME: self._workbook.add_format({"num_format": "mm:ss.000"}),
            SessionDashboard.DT_TIME_DELTA: self._workbook.add_format({"num_format": "0.000"}),
        }
        self._header_format = self._workbook.add_format({
            "bg_color": "#C5D9F1",
            "bold": True,
        })
        self._row_count = 1


    def write(self, dashboard):
        self._write_header(dashboard)
        for lap in dashboard.laps:
            self._write_lap(dashboard, lap)
        self._workbook.close()


    def _write_header(self, dashboard):
        self._worksheet.set_column(0, len(dashboard.columns), 12)
        for i, column in enumerate(dashboard.columns):
            self._worksheet.write_string(0, i, column.title, self._header_format)


    def _write_lap(self, dashboard, lap_register):
        for i, (measure_id, title, datatype) in enumerate(dashboard.columns):
            if measure_id in lap_register:
                value = lap_register[measure_id]
                xls_value = self._convert_value(value, datatype)
            else:
                xls_value = "-"
            xls_format = self._get_cell_format(datatype)
            self._worksheet.write(self._row_count, i, xls_value, xls_format)
        self._row_count += 1


    def _get_cell_format(self, datatype):
        return self._type_formats.get(datatype)


    @staticmethod
    def _convert_value(value, datatype):
        if datatype == SessionDashboard.DT_LAP_TIME:
            return value / 86400
        elif datatype == SessionDashboard.DT_FLAG:
            return "X" if value else ""
        else:
            return value


