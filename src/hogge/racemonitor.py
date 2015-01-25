from time import sleep


class RaceMonitor(object):

    QUERY_INTERVAL = 0.1
    LAP_TIME_QUERY_DELAY = 2  #Last lap time info doesn't update instantaneous. Set a delay to workaround this.
    LAP_TIME_QUERY_RETRIES = 3  #Last lap time info doesn't update instantaneous. Set a delay to workaround this.

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
        self._session_dashboard.name = self.get_session_name()
        current_lap = telemeter["Lap"]
        pitted = False
        while telemeter.is_connected:
            ir_lap = telemeter["Lap"]
            is_pit = telemeter["OnPitRoad"]
            if is_pit:
                pitted = True
            if ir_lap > current_lap:
                self.save_last_lap(current_lap, pitted)
                current_lap = ir_lap
                pitted = False
            else:
                sleep(self.QUERY_INTERVAL)



    def wait_for_telemeter(self):
        while not self._telemeter.startup():
            sleep(3)


    def save_last_lap(self, lap, pitted):
        telemeter = self._telemeter
        lap_register = {"Lap": lap, "Pitted": pitted}
        for measure_id, _, _ in self._session_dashboard.columns:
            if measure_id in ["Lap", "LapLastLapTime"]:
                continue
            value = telemeter[measure_id]
            if value is not None:
                lap_register[measure_id] = value
        # Save Lap Time
        last_lap_time = None
        for i in range(self.LAP_TIME_QUERY_RETRIES):
            sleep(self.LAP_TIME_QUERY_DELAY)
            last_lap_time = telemeter["LapLastLapTime"]
            if last_lap_time > 0:
                break
        if last_lap_time is not None:
            lap_register["LapLastLapTime"] = last_lap_time
        self._session_dashboard.add_lap(lap_register)


    def get_session_name(self):
        from datetime import datetime
        telemeter = self._telemeter
        car = telemeter["DriverInfo"]["Drivers"][0]["CarScreenNameShort"]
        session_type = telemeter["SessionInfo"]["Sessions"][0]["SessionType"]
        track = telemeter["WeekendInfo"]["TrackName"]
        time = datetime.now().strftime("%Y%m%d-%H%M")
        return "{0} @ {1} - {2} ({3})".format(car, track, time, session_type)
