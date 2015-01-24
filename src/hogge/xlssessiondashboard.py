from collections import namedtuple
import xlsxwriter


DashboardColumn = namedtuple("Dashboard", ["measure_id", "title", "datatype"])

class XlsSessionDashboard(object):

    def __init__(self, excel_filename):
        self.columns = []
        self._calculators = {}
        self._laps = []

        self._row_count = 1
        self._workbook = xlsxwriter.Workbook(excel_filename)
        self._worksheet = self._workbook.add_worksheet()
        self._time_format = self._workbook.add_format({"num_format": "mm:ss.000"})


    @classmethod
    def create_default_dashboard(cls, xls_filename):
        dashboard = XlsSessionDashboard(xls_filename)
        dashboard.add_column(measure_id="Lap", title="Lap", datatype=None)
        dashboard.add_column(measure_id="LapLastLapTime", title="Time", datatype="time")
        dashboard.add_column(measure_id="LapLastLapDelta", title="Dif", datatype=None)
        dashboard.add_column(measure_id="FuelLevel", title="Fuel", datatype=None)
        dashboard.add_column(measure_id="FuelConsumption", title="Consumption", datatype=None)
        dashboard.add_calculator("LapLastLapDelta", calculate_last_lap_delta)
        dashboard.add_calculator("FuelConsumption", calculate_fuel_consumption)
        return dashboard


    def add_column(self, **kwargs):
        self.columns.append(DashboardColumn(**kwargs))


    def save_lap(self, lap_register):
        if not self._laps:
            self._write_header()
        self._laps.append(lap_register)
        self._write_lap(lap_register)


    def close_dashboard(self):
        self._workbook.close()


    def _write_header(self):
        for i, column in enumerate(self.columns):
            self._worksheet.write(0, i, column.title)


    def _write_lap(self, lap_register):
        for i, (measure_id, title, datatype) in enumerate(self.columns):
            if measure_id in lap_register:
                value = lap_register[measure_id]
            elif measure_id in self._calculators:
                calculator = self._calculators[measure_id]
                value = calculator(self._laps)
            else:
                value = "-"
            xls_format = self._get_cell_format(datatype)
            xls_value = self._convert_value(value, datatype)
            self._worksheet.write(self._row_count, i, xls_value, xls_format)
        self._row_count += 1


    def _get_cell_format(self, datatype):
        if datatype == "time":
            return self._time_format
        else:
            return None


    def _convert_value(self, value, datatype):
        if datatype == "time":
            return value / 86400
        else:
            return value

    def add_calculator(self, param, calculator):
        self._calculators[param] = calculator


def calculate_fuel_consumption(lap_table):
    if len(lap_table) >= 2:
        return lap_table[-2]["FuelLevel"] - lap_table[-1]["FuelLevel"]


def calculate_last_lap_delta(lap_table):
    if len(lap_table) >= 2:
        return lap_table[-1]["LapLastLapTime"] - lap_table[-2]["LapLastLapTime"]
