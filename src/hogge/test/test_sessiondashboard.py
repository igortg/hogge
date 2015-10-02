from hogge.sessiontimesheet import SessionTimeSheet


def test_dashboard():
    dashboard = SessionTimeSheet.create_default_timesheet()

    dashboard.add_lap(dict(Lap=1, LapLastLapTime=68.392, FuelLevel=12.0))
    dashboard.add_lap(dict(Lap=2, LapLastLapTime=69.584, FuelLevel=11.2))

    lap2 = dashboard.laps[1]
    assert lap2["Lap"] == 2
    assert round(lap2["LapLastLapDelta"], 3) == 1.192
    assert round(lap2["FuelConsumption"], 3) == 0.8
