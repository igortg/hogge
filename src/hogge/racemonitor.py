from time import sleep
from hogge.sessiondashboard import SessionDashboard


class RaceMonitor(object):

    QUERY_INTERVAL = 0.1

    def __init__(self, ir_sdk, output_stream):
        self._ir_sdk = ir_sdk
        dashboard = SessionDashboard(output_stream)
        dashboard.add_column("lap", "Lap", None)
        dashboard.add_column("lap_time", "Time", None)
        dashboard.add_column("fuel", "Fuel", None)
        self._session_table = dashboard


    def start(self):
        ir = self._ir_sdk
        if not ir.startup():
            raise RuntimeError("Couldn't start iRacing connection")
        else:
            print("Connected to iRacing")
        current_lap = ir["Lap"]
        while ir.is_connected:
            ir_lap = ir["Lap"]
            if ir_lap == current_lap:
                sleep(self.QUERY_INTERVAL)
                continue
            self.save_lap(current_lap, ir)
            current_lap = ir_lap


    def save_lap(self, lap, ir_data):
        lap_register = dict(
            lap=lap,
            fuel=ir_data["FuelLevel"],
        )
        sleep(1)
        lap_register["lap_time"] = ir_data["LapLastLapTime"]

        self._session_table.save_lap(lap_register)
