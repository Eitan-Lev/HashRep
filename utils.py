
#returns file as lines list
def readfile(file):
    with open(file,'r') as fh:
        lines = fh.readlines()
        lines = [x.rstrip('\n') for x in lines]
        return lines



class Car:
    def __init__(self, id ):
        self.id = id
        self.rides = []

    def getTavilable(self):

        if not self.rides:
            return 0

        return self.rides[-1].tEnd

    def addRide(self, ride):
        self.rides.append(ride)

    def getPosition(self):
        if not self.rides:
            return 0, 0

        return self.rides[-1].endLoc


class Ride:

    def __init__(self, id, startLoc, endLoc, tStart, tEnd, bonus ):

        self.id = id
        self.startLoc = startLoc
        self.endLoc = endLoc
        self.tStart = tStart
        self.tEnd = tEnd
        self.bonus = bonus

def initRides(rides):

    ridesMap = {}
    for ride in rides:
        ridesMap[ride.id] = ride #Rides is a Ride list
    return ridesMap

def manhattenDistance(startLoc, endLoc):

   x1, y1 = startLoc
   x2, y2 = endLoc
   return abs(x1 - x2) + (y1 - y2)


def isValidRide(ride, car):


    position = car.getPosition()

    arrivalTime = manhattenDistance(position, ride.startLoc)
    rideTime = manhattenDistance(ride.startLoc, ride.endLoc)

    if (car.getTavilable() + arrivalTime + rideTime) > ride.tEnd:
        return False

    return True

class RidesList:

    def __init__(self, rides):
        self.ridesMap = initRides(rides)



    def getLeastIdleTimeRide(self, car):

        carAvailable = car.getTavilable()
        carPosition = car.getPosition()


        #Search the ride closest to the position, that minimizes the waiting time.
        distancesRideTupList = [(manhattenDistance(carPosition, ride.startLoc) + max(ride.tStart - carAvailable,0), ride) for ride in self.ridesMap.values()]
        sortedDistance = sorted(distancesRideTupList, key = lambda tup: tup[0])

        return self.ridesMap.pop(sortedDistance[0][1].id)


def createOutputFile(outputFilePath, carsList):

    lines = []

    for car in carsList:
        curLine = str(len(car.rides)) + ' '
        for ride in car.rides:
            curLine+= str(ride.id) + ' '
        lines.append(curLine + '\n')

    with open(outputFilePath, 'w')  as fh:
        fh.writelines(lines)




EXAMPLE_FILE = r'a_example.in'
METROPOLICE_FILE = r'd_metropolis.in'
OUTPUT_FILE = r'output.out'

def main():
    fileLines = readfile(METROPOLICE_FILE)
    firstLine = fileLines[0]
    firstLinesSplited = firstLine.split(' ')
    firstLinesSplited = [int(x) for x in firstLinesSplited]
    carsNum = firstLinesSplited[2]
    ridesNum = firstLinesSplited[3]
    bonus = firstLinesSplited[4]
    totalTime = firstLinesSplited[5]

    carsList = [Car(x) for x in range(carsNum)]

    rides = []
    count = 0
    for line in fileLines[1:]:
        linesSplit = line.split(' ')
        linesSplit = [int(x) for x in linesSplit]

        startLoc = linesSplit[0], linesSplit[1]
        endLoc = linesSplit[2], linesSplit[3]
        tStart=  linesSplit[4]
        tEnd=  linesSplit[5]
        rides.append(Ride(count, startLoc, endLoc, tStart, tEnd, bonus))
        count+=1

    ridesList = RidesList(rides)




    carIdx = 0
    while ridesList.ridesMap:

        curCar = carsList[carIdx]
        curCar.addRide(ridesList.getLeastIdleTimeRide(curCar))

        carIdx = (carIdx +1) % carsNum


    createOutputFile(OUTPUT_FILE, carsList)

main()

