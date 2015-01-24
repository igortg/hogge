from hogge.racemonitor import RaceMonitor
from hogge.xlssessiondashboard import XlsSessionDashboard


def test_racemonitor(tmpdir, irsdk):
    xls_file = tmpdir.mkdir("hogge").join("session.xlsx")
    dashboard = XlsSessionDashboard.create_default_dashboard(str(xls_file))
    hogge = RaceMonitor(irsdk, dashboard)
    hogge.start()
    import os; os.startfile(str(xls_file))