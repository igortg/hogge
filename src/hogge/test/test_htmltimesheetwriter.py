#-*- coding: utf8
from hogge.htmltimesheetwriter import HtmlTimeSheetWriter
from hogge.sessiontimesheet import SessionTimeSheet
import os


def test_htmldashboardwriter():
    test_dirname = os.path.dirname(__file__)
    timesheet = SessionTimeSheet.create_default_timesheet()
    timesheet.add_lap(dict(Lap=1, LapLastLapTime=60, FuelLevel=12.0))
    timesheet.add_lap(dict(Lap=2, LapLastLapTime=62.500, FuelLevel=10.4))
    timesheet.add_lap(dict(Lap=3, LapLastLapTime=64, FuelLevel=9))
    timesheet.add_lap(dict(Lap=4, LapLastLapTime=95.312, FuelLevel=12)) #Refuel
    timesheet.add_lap(dict(Lap=5, LapLastLapTime=-1, FuelLevel=-1))

    writer = HtmlTimeSheetWriter()
    writer.dump(timesheet, os.path.join(test_dirname, "test-sheet.html"))