import pytest
import irsdk


@pytest.fixture(scope="module")
def irsdk_mock():
    return IRSDKMock()


class IRSDKMock(object):

    def __init__(self):
        self.data = MOCK_DATA[:]
        self._query_index = 0


    def __getitem__(self, item):
        return MOCK_DATA[self._query_index].get(item, None)


    def startup(self):
        return True


    @property
    def is_connected(self):
        self._query_index += 1
        return self._query_index < len(MOCK_DATA)


MOCK_DATA = [
    dict(
        Lap=0,
        FuelLevel=12,
        LapLastLapTime=0,
        OnPitRoad=0,
        CarIdxTrackSurface=[0],
        IsOnTrack=True,
        SessionState=irsdk.SessionState.racing,
        DriverInfo={"DriverCarIdx": 0}
    )
]

for i in range(1, 10):
    MOCK_DATA.append(
        dict(
            Lap=i // 3,
            FuelLevel=12.0 - (i * 0.5),
            LapLastLapTime=68.32 + (i * 0.1),
            OnPitRoad=0,
            CarIdxTrackSurface=[0],
            IsOnTrack=True,
            SessionState=irsdk.SessionState.racing,
            DriverInfo={"DriverCarIdx": 0}
        )
    )
MOCK_DATA.append(
    dict(
        Lap=4,
        FuelLevel=12,
        LapLastLapTime=-1,
        OnPitRoad=1,
        CarIdxTrackSurface=[0],
        IsOnTrack=True,
        SessionState=irsdk.SessionState.racing,
        DriverInfo={"DriverCarIdx": 0}
    )
)
