import os
from hogge.htmltimesheetwriter import HtmlTimeSheetWriter
from hogge.racemonitor import RaceMonitor
from hogge.sessiontimesheet import SessionTimeSheet


def test_racemonitor(irsdk_mock):
    dashboard = SessionTimeSheet.create_default_timesheet()
    hogge = RaceMonitor(irsdk_mock)
    hogge.MONITOR_FREQ = 600
    hogge._timesheet = dashboard
    hogge.start()

    lap1 = dashboard.laps[1]
    assert round(lap1["LapLastLapTime"], 2) == 68.92