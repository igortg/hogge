from time import sleep


class RaceMonitor(object):

    LAP_TIME_QUERY_DELAY = 2  #Last lap time info doesn't update instantaneous. Set a delay to workaround this.
    LAP_TIME_QUERY_RETRIES = 3  #Last lap time info doesn't update instantaneous. Set a delay to workaround this.

    def __init__(self, telemeter, timesheet, on_lap_callback=None):
        """

        :param IRSDK telemeter: measure car and session data.

        :param SessionTimeSheet timesheet: store session data and write it to disk.

        :param callable on_lap_callback: function which will be called on a lap is completed.
        """
        self._telemeter = telemeter
        self._timesheet = timesheet
        self._on_lap_callback = on_lap_callback
        self.query_interval = 1


    def start(self):
        telemeter = self._telemeter
        if not telemeter.startup():
            raise RuntimeError("Couldn't start iRacing connection")
        try:
            self._timesheet.name = self.get_session_name()
        except TypeError:
            self._timesheet.name = "unnamed"
        lap_register = {"Lap": telemeter["Lap"]}
        while telemeter.is_connected:
            sleep(self.query_interval)
            if telemeter["IsReplayPlaying"]:
                continue
            self._query_lap_events(lap_register)
            # Check if start/finish line was crossed
            if telemeter["Lap"] > lap_register["Lap"] :
                self.save_previous_lap(lap_register)
                if self._on_lap_callback is not None:
                    self._on_lap_callback(lap_register)
                lap_register = {"Lap": telemeter["Lap"]}


    def wait_for_telemeter(self):
        while not self._telemeter.startup():
            sleep(3)


    def save_previous_lap(self, lap_register):
        telemeter = self._telemeter
        for measure_id, _, _ in self._timesheet.columns:
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
        self._timesheet.add_lap(lap_register)


    def _query_lap_events(self, lap_register):
        telemeter = self._telemeter
        if telemeter["OnPitRoad"]:
            lap_register["HasPitted"] = True
        if telemeter["CarIdxTrackSurface"]:
            lap_register["IsCleanLap"] = False


    def get_session_name(self):
        from datetime import datetime
        telemeter = self._telemeter
        car = telemeter["DriverInfo"]["Drivers"][0]["CarScreenNameShort"]
        session_type = telemeter["SessionInfo"]["Sessions"][0]["SessionType"]
        track = telemeter["WeekendInfo"]["TrackName"]
        time = datetime.now().strftime("%Y%m%d-%H%M")
        return "{0} @ {1} - {2} ({3})".format(car, track, time, session_type)
