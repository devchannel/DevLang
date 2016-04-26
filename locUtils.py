def nextLine(loc):
    loc = (loc[0] + 1, loc[1])
    return loc


def nextColumn(loc):
    loc = (loc[0], loc[1] + 1)
    return loc


def moveLineBy(loc, n):
    loc = (loc[0] + n, loc[1])
    return loc


def moveColumnBy(loc, n):
    loc = (loc[0], loc[1] + n)
    return loc


def setLine(loc, n):
    loc = (n, loc[1])
    return loc


def setColumn(loc, n):
    loc = (loc[0], n)
    return loc
