import os
from hogge.htmltimesheetwriter import HtmlTimeSheetWriter
from hogge.racemonitor import RaceMonitor
from hogge.sessiontimesheet import SessionTimeSheet


def test_racemonitor(irsdk):
    test_dirname = os.path.dirname(__file__)
    dashboard = SessionTimeSheet.create_default_timesheet()
    hogge = RaceMonitor(irsdk, dashboard)
    hogge.start()

    lap1 = dashboard.laps[1]
    assert round(lap1["LapLastLapTime"], 2) == 68.92