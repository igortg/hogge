from hogge.xlssessiondashboard import XlsSessionDashboard


def test_dashboard(tmpdir):
    output_file = tmpdir.mkdir("hogge").join("session.xlsx")
    dashboard = XlsSessionDashboard.create_default_dashboard(str(output_file))

    dashboard.save_lap(dict(lap=1, LapLastLapTime=68.392, FuelLevel=12.0))
    dashboard.save_lap(dict(lap=2, LapLastLapTime=69.584, FuelLevel=11.2))
    dashboard.close_dashboard()
    import os; os.startfile(str(output_file))