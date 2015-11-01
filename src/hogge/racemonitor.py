from time import sleep


class RaceMonitor(object):

    LAP_TIME_QUERY_DELAY = 3  #Last lap time info doesn't update instantaneous. Set a delay to workaround this.
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
        self._last_read_lap_time = None


    def start(self):
        telemeter = self._telemeter
        if not telemeter.startup():
            raise RuntimeError("Couldn't start iRacing connection")
        lap_register = self._create_lap_register(telemeter["Lap"])
        while telemeter.is_connected:
            sleep(self.query_interval)
            if not telemeter["IsOnTrack"]:
                continue
            self._query_lap_events(lap_register)
            # Check if start/finish line was crossed
            if telemeter["Lap"] > lap_register["Lap"] :
                self.save_previous_lap(lap_register)
                if self._on_lap_callback is not None:
                    self._on_lap_callback(lap_register)
                lap_register = self._create_lap_register(telemeter["Lap"])


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
        if telemeter["OnPitRoad"]:
            lap_register["HasPitted"] = True
        # Save Lap Time, "LapLastLapTime" has a delay of few seconds to be update, so we wait and check if it changed
        sleep(self.LAP_TIME_QUERY_DELAY)
        for i in range(self.LAP_TIME_QUERY_RETRIES):
            last_lap_time = telemeter["LapLastLapTime"]
            if last_lap_time != self._last_read_lap_time:
                self._last_read_lap_time = last_lap_time
                lap_register["LapLastLapTime"] = last_lap_time if last_lap_time > 0 else 0
                self._timesheet.add_lap(lap_register)
                break
            else:
                sleep(self.query_interval)


    @staticmethod
    def _create_lap_register(lap):
        return {
            "Lap": lap,
            "HasPitted": False,
            "HasOffTrack": False,
        }


    def _query_lap_events(self, lap_register):
        telemeter = self._telemeter
        driver_index = telemeter["DriverInfo"]["DriverCarIdx"]
        if telemeter["CarIdxTrackSurface"][driver_index] == 0:
            lap_register["HasOffTrack"] = True


    def get_session_name(self):
        from datetime import datetime
        telemeter = self._telemeter
        driver_index = telemeter["DriverInfo"]["DriverCarIdx"]
        driver_data = telemeter["DriverInfo"]["Drivers"][driver_index]
        car = driver_data["CarScreenNameShort"]
        driver_name = driver_data["UserName"]
        session_type = telemeter["SessionInfo"]["Sessions"][0]["SessionType"]
        track = telemeter["WeekendInfo"]["TrackName"]
        time = datetime.now().strftime("%y%m%d-%H%M")
        return "{0} @ {1} - {2} ({3})".format(car, track, time, driver_name)
