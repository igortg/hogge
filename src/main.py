import random
from hogge.hogge import Hogge, HOGGE_QUOTES


def print_title():
    print("== Hogge - iRacing Session Lap Chronometer ==")
    print()
    print('\t"{0}"'.format(random.choice(HOGGE_QUOTES)))
    print()


if __name__ == '__main__':
    print_title()
    app = Hogge()
    app.main()