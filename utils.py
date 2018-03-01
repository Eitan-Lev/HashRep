INFINITY = 10**10

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
   return abs(x1 - x2) + abs(y1 - y2)


def isValidRide(ride, car):


    carAvailable = car.getTavilable()
    carPosition = car.getPosition()

    gettingThereDistance =  manhattenDistance(carPosition, ride.startLoc)

    #Calc waitingTime:

    gettingThereTime = carAvailable + gettingThereDistance
    waitingTime =  max(ride.tStart - gettingThereTime,0)

    endingRideTime = gettingThereTime + waitingTime + manhattenDistance(ride.startLoc, ride.endLoc)

    if endingRideTime > ride.tEnd:
        return False
    else:
        return True


class RidesList:

    def __init__(self, rides):
        self.ridesMap = initRides(rides)

    def getLeastIdleTimeRide(self, car):

        carAvailable = car.getTavilable()
        carPosition = car.getPosition()


        #Search the ride closest to the position, that minimizes the waiting time.

        distancesRideTupList = [(dorAlonValue(car, ride), ride) for ride in self.ridesMap.values()]
        selectedValue = min(distancesRideTupList, key = lambda tup: tup[0])

        return self.ridesMap.pop(selectedValue[1].id)


def dorAlonValue(car, ride):

    carAvailable = car.getTavilable()
    carPosition = car.getPosition()

    gettingThereDistance =  manhattenDistance(carPosition, ride.startLoc)

    #Calc waitingTime:

    gettingThereTime = carAvailable + gettingThereDistance
    waitingTime =  max(ride.tStart - gettingThereTime,0)


    endingRideTime = gettingThereTime + waitingTime + manhattenDistance(ride.startLoc, ride.endLoc)
    value = gettingThereTime + waitingTime

    #Check if we get bonus
    if gettingThereTime <= ride.tStart:
        value -= ride.bonus


    if endingRideTime > ride.tEnd:
        return INFINITY
    else:
        return value

def dorEitanValue(car, ride):

    carAvailable = car.getTavilable()
    carPosition = car.getPosition()

    gettingThereDistance =  manhattenDistance(carPosition, ride.startLoc)

    #Calc waitingTime:

    gettingThereTime = carAvailable + gettingThereDistance
    waitingTime =  max(ride.tStart - gettingThereTime,0)

    endingRideTime = gettingThereTime + waitingTime + manhattenDistance(ride.startLoc, ride.endLoc)

    if endingRideTime > ride.tEnd:
        return INFINITY
    else:
        return gettingThereTime + waitingTime



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
EASY_FILE = r'b_should_be_easy.in'
HURRY_FILE = r'c_no_hurry.in'
BONUS_FILE = r'e_high_bonus.in'

# OUTPUT_FILE = r'output.out'

def createSingleExperiment(inputFile):
    fileLines = readfile(inputFile)
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
    prevLen = len(ridesList.ridesMap)
    justStarted = True
    while ridesList.ridesMap:

        if (carIdx == 0):
            curLen = len(ridesList.ridesMap)
            if (not justStarted and curLen == prevLen): #If thee were no changes, stop iterating
                break
            justStarted = False
            prevLen = curLen

        curCar = carsList[carIdx]
        selectedRide = ridesList.getLeastIdleTimeRide(curCar)
        if isValidRide(selectedRide, curCar):
            curCar.addRide(selectedRide)

        carIdx = (carIdx +1) % carsNum

    outputFile = inputFile.split('.')[0] + '.out'
    createOutputFile(outputFile, carsList)

def main():
    # INPUT_FILES_LIST = [EXAMPLE_FILE, BONUS_FILE, HURRY_FILE, EASY_FILE, METROPOLICE_FILE]
    INPUT_FILES_LIST = [EXAMPLE_FILE]
    for f in INPUT_FILES_LIST:
        print('Starting file:', f)
        createSingleExperiment(f)

main()