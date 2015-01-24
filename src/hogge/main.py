import irsdk
import sys
from hogge.racemonitor import RaceMonitor


def main():
    ir = irsdk.IRSDK()
    output = sys.__stdout__
    hogge = RaceMonitor(ir, output)
    hogge.start()






if __name__ == '__main__':
    main()