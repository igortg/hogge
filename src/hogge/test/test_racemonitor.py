import os
from hogge.htmltimesheetwriter import HtmlTimeSheetWriter
from hogge.racemonitor import RaceMonitor
from hogge.sessiontimesheet import SessionTimeSheet


def test_racemonitor(irsdk):
    test_dirname = os.path.dirname(__file__)
    dashboard = SessionTimeSheet.create_default_timesheet()
    html_writer = HtmlTimeSheetWriter("test-sheet", test_dirname)
    hogge = RaceMonitor(irsdk, dashboard, html_writer)
    hogge.start()

    lap1 = dashboard.laps[1]
    assert round(lap1["LapLastLapTime"], 2) == 68.92