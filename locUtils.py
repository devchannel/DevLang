def nextLine(location):
    return (location[0] + 1, location[1])


def nextColumn(location):
    return (location[0], location[1] + 1)


def moveLineBy(location, n):
    return (location[0] + n, location[1])


def moveColumnBy(location, n):
    return (location[0], location[1] + n)


def setLine(location, n):
    return (n, location[1])


def setColumn(location, n):
    return (location[0], n)
