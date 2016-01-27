from hogge.sessiontimesheet import SessionTimeSheet


def test_timesheet():
    timesheet = SessionTimeSheet.create_default_timesheet()

    timesheet.add_lap(dict(Lap=1, LapLastLapTime=60, FuelLevel=12.0))
    timesheet.add_lap(dict(Lap=2, LapLastLapTime=62.500, FuelLevel=10.4))
    timesheet.add_lap(dict(Lap=3, LapLastLapTime=64, FuelLevel=9))
    timesheet.add_lap(dict(Lap=4, LapLastLapTime=95.312, FuelLevel=12)) #Refuel
    timesheet.add_lap(dict(Lap=5, LapLastLapTime=-1, FuelLevel=-1))


    lap2 = timesheet.laps[1]
    assert lap2["Lap"] == 2
    assert round(lap2["LapLastLapDelta"], 3) == 2.5
    assert round(lap2["FuelConsumption"], 3) == 1.6
    lap4 = timesheet.laps[3]
    assert round(lap4["FuelConsumption"], 3) == 0

    summary = timesheet.create_summary()
    assert summary["AvgFuelConsumption"] == 1.5
    assert round(summary["AvgFuelConsumptionPerMin"], 2) == 1.42
    assert round(summary["AvgLapTime"], 2) == 70.45
    assert round(summary["AvgLapTime"], 2) == 70.45
    assert round(summary["AvgBestLapTime"], 2) == 62.17