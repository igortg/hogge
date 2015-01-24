from time import sleep


class RaceMonitor(object):

    QUERY_INTERVAL = 0.1

    def __init__(self, telemeter, dashboard):
        """

        :param IRSDK telemeter: measure car and session data

        :param XlsSessionDashboard dashboard: store session data and write it to disk
        """
        self._telemeter = telemeter
        self._session_dashboard = dashboard


    def start(self):
        telemeter = self._telemeter
        if not telemeter.startup():
            raise RuntimeError("Couldn't start iRacing connection")
        current_lap = telemeter["Lap"]
        while telemeter.is_connected:
            ir_lap = telemeter["Lap"]
            if ir_lap > current_lap:
                self.save_lap(current_lap)
                current_lap = ir_lap
            else:
                sleep(self.QUERY_INTERVAL)



    def wait_for_telemeter(self):
        while not self._telemeter.startup():
            sleep(3)


    def save_lap(self, lap):
        telemeter = self._telemeter
        lap_register = {"Lap": lap}
        for measure_id, _, _ in self._session_dashboard.columns:
            if measure_id in ["Lap", "LapLastLapTime"]:
                continue
            value = telemeter[measure_id]
            if value is not None:
                lap_register[measure_id] = value
        sleep(1)
        lap_register["LapLastLapTime"] = telemeter["LapLastLapTime"]
        self._session_dashboard.save_lap(lap_register)
