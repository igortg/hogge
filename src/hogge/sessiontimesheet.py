from collections import namedtuple


DashboardColumn = namedtuple("DashboardColumn", ["measure_id", "title", "datatype"])

class SessionTimeSheet(object):

    DT_INT = "int"
    DT_FLOAT = "float"
    DT_LAP_TIME = "laptime"
    DT_TIME_DELTA = "timedelta"
    DT_FLAG = "flag"

    def __init__(self):
        self.name = "<unnamed>"
        self.columns = []
        self._calculators = {}
        self._laps = []
        self._row_count = 1


    @classmethod
    def create_default_timesheet(cls):
        dashboard = SessionTimeSheet()
        dashboard.add_column(measure_id="Lap", title="Lap", datatype=cls.DT_INT)
        dashboard.add_column(measure_id="LapLastLapTime", title="Time", datatype=cls.DT_LAP_TIME)
        dashboard.add_column(measure_id="LapLastLapDelta", title="Delta", datatype=cls.DT_TIME_DELTA)
        dashboard.add_column(measure_id="FuelLevel", title="Fuel", datatype=cls.DT_FLOAT)
        dashboard.add_column(measure_id="FuelConsumption", title="Consumption", datatype=cls.DT_FLOAT)
        dashboard.add_column(measure_id="Pitted", title="Pitted", datatype=cls.DT_FLAG)
        dashboard.add_column(measure_id="OffTrack", title="Off Track", datatype=cls.DT_FLAG)
        dashboard.add_calculator("LapLastLapDelta", calculate_last_lap_delta)
        dashboard.add_calculator("FuelConsumption", calculate_fuel_consumption)
        return dashboard


    def add_column(self, **kwargs):
        self.columns.append(DashboardColumn(**kwargs))


    def add_lap(self, lap_register):
        self._laps.append(lap_register)
        for i, (measure_id, title, datatype) in enumerate(self.columns):
            if measure_id in self._calculators:
                calculator = self._calculators[measure_id]
                value = calculator(self._laps)
                lap_register[measure_id] = value
            elif measure_id not in lap_register:
                lap_register[measure_id] = None


    @property
    def laps(self):
        return self._laps[:]


    def add_calculator(self, param, calculator):
        self._calculators[param] = calculator


    def create_summary(self):
        summary = {
            "TotalLapTime": 0,
            "TotalFuelConsumption": 0,
        }
        lap_count =  len(self.laps)
        for lap in self.laps:
            summary["TotalLapTime"] += lap["LapLastLapTime"]
            summary["TotalFuelConsumption"] += lap["FuelConsumption"]
        summary["AvgFuelConsumption"] = summary["TotalFuelConsumption"] / lap_count if lap_count else 0
        summary["AvgFuelConsumptionPerMin"] = summary["TotalFuelConsumption"] / (summary["TotalLapTime"] / 60.0) if summary["TotalLapTime"] else 0
        return summary



def calculate_fuel_consumption(lap_table):
    if len(lap_table) >= 2:
        return lap_table[-2]["FuelLevel"] - lap_table[-1]["FuelLevel"]
    else:
        return 0


def calculate_last_lap_delta(lap_table):
    if len(lap_table) >= 2:
        return lap_table[-1]["LapLastLapTime"] - lap_table[-2]["LapLastLapTime"]
    else:
        return 0
