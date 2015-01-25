from hogge.racemonitor import RaceMonitor
from hogge.sessiondashboard import SessionDashboard


def test_racemonitor(irsdk):
    dashboard = SessionDashboard.create_default_dashboard()
    hogge = RaceMonitor(irsdk, dashboard)
    hogge.start()

    lap1 = dashboard.laps[1]
    assert round(lap1["LapLastLapTime"], 2) == 68.92