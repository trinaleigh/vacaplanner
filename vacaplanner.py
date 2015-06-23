from traveldata import *

class destination(object):
    """
    Represents a trip destination and holds information about the location,
    including the cost of lodging and cost of travel from New York City.
    """
    def __init__(self,name):
        self.name=name
        #create empty placeholders for the key attributes of a desination:
        self.travelCost=[]
        self.lodgingCost=[]
        self.temperatures=[]
        self.rainfall=[]
        # weather vars (temp and rainfall) are not being used yet
    def updateCosts(self,travelCost,lodgingCost):
        """
        adds travel cost information to the destination
        """
        if len(travelCost) != 12 or len(lodgingCost) != 12:
            raise ValueError('Costs should be in the format of 12 monthly averages')
        for i in travelCost:
            self.travelCost.append(float(i))
        for i in lodgingCost:
            self.lodgingCost.append(float(i))
        
    def updateWeather(self,temperatures,rainfall):
        """
        adds weather information to the destination
        """
        if len(temperatures) != 12 or len(rainfall) !=12:
            raise ValueError('Weather Data should be in the format of 12 monthly averages')
        for i in temperatures:
            self.temperatures.append(float(i))
        for i in rainfall:
            self.rainfall.append(float(i))
  


    def findBestMonth(self, tripLength):
        """
        returns a tuple with the best month and price for a given trip length
        """
              
        def createTrips(tripLength):
            """
            Returns a dictionary of possible trips to a destination
            
            For a given length of stay, considers the travel & loding costs for 
            each month of the year  to compute the total cost of  possible trips
            
            Resulting dictionary structure:
                Keys are months, numbered 1-12
                Values are total trip costs for the given length of stay
            """
            # create an empty dictionary
            possibleTrips={}
            # for each month
            for month in range(1,13):
                # populate the possible trips
                possibleTrips[month]=((tripLength*self.lodgingCost[month-1])+self.travelCost[month-1])
            
            return possibleTrips
            
        # find the lowest price
        monthlyData = createTrips(tripLength)
        bestPrice = min(monthlyData.values())
        for month, price in monthlyData.items():
            if price == bestPrice:
                bestMonth = month
                # note: when there are ties, this process favors months that are later the year. 
                # this should be less of a problem with real cost data (ties unlikely)
        return (bestMonth, bestPrice)
            
    def __str__(self):
        return self.name

def buildDestinations(destinations):
    """
    build the required destination classes from user-input requests
    """
    builtDestinations=[]
    for i in destinations:
        # print i
        newDest = destination(i)
        newDest.updateCosts(costDB[i][0],costDB[i][1])
        builtDestinations.append(newDest)
    return builtDestinations

def tripDivisions(maxLength):
    """
    given the user's total vacation allowance,
    returns possible divisions of their time on each trip
    
    ASSUMPTIONS:
        - I want to maximize the number of full-week trips I can take. First,
        find the max number of times I can use 5 vacation days.  Assume that each 
        time I use 5 vacation days, I'm taking a 9-day trip (using the weekends on
        either side).
        - With any remaining days, I'll take long weekends.  Assume that each 
        time I use a single vacation day, I'm taking a 3-day trip (long weekend).
    
    returns a list of possible divisions among the destinations
    (number of days at each destination)
    
    """   
    
    # find number of long trips
    longTrips=maxLength/5
    # find number of short trips
    shortTrips=maxLength%5
    # return the list   
    tripDivisions=[]
    for i in range(longTrips):
        tripDivisions.append(9) 
    for i in range(shortTrips):
        tripDivisions.append(3)      
    return tripDivisions


def optimizeYear(tripDivisions,destinations):
    
    def tripOrders(destinations):
        """
        produces all possible permutations for the list of destinations
        will be used later to map destinations to the length of stay at each
        """
        def permutations(inputList):
            # if the length is 1, there is only one permutation
            if len(inputList) ==1:
                yield inputList
            # if the length is 2, there are only 2 permutations (swapped)
            elif len(inputList) == 2:
                yield inputList
                reverse = [inputList[1], inputList[0]]
                yield reverse
            else:
                for i in range(0, len(inputList)):
                    # find all permutations begging with "i"
                    for p in permutations(inputList[0:i] + inputList[i+1:len(inputList)]):
                        yield [inputList[i]] + p
    
        options=[]
        for order in permutations(destinations):
            options.append(order)
        return options
   
    # for each trip order
    toTest=tripOrders(destinations)
    bestCost=1000000
    # note - could replace bestCost with a user-input max budget
    bestSchedule={}
    for arrangement in toTest:
        # using trip divisions, find the total cost association 
        # find total cost
        tempSchedule=[]
        tempCost=0
        for i in range(len(tripDivisions)):
            # fill in the tempSchedule list
            # [destination, length of stay, month of travel, cost of trip]
            tempSchedule.append([str(arrangement[i])]+[tripDivisions[i],]+[arrangement[i].findBestMonth(tripDivisions[i])[0]]+[arrangement[i].findBestMonth(tripDivisions[i])[1]])
            tempCost+=tempSchedule[-1][-1]
        if tempCost < bestCost:
            bestCost = tempCost
            bestSchedule = tempSchedule
    months={1:"January",2:"February",3:"March",4:"April",5:"May",6:"June",7:"July",8:"August",9:"September",10:"October",11:"November",12:"December"}
    
    print "Here's your schedule:"
    for i in bestSchedule:
        print "- Trip to " +  i[0] + " for " + str(i[1]) + " days in " + months[i[2]] + ", costing " + str(i[3]) + " dollars total."          
    print "Total vacation cost for the year is " + str(bestCost) + " dollars."
    print "Have fun!"
    

def play():
    """Allows the user to enter trip preferences and find the optimized plan.
    
    - Loads data
    - Provides an intro description
    - Asks the user information about how much time they have to spend
    - Asks the user to add potential destinations
    - When the user is done entering preferences, find the optimal vacation
    
    """
    while True:
        days = raw_input('How many vacations days do you have available over the next year?')
        try:
            divisions=tripDivisions(int(days))
            print('Great! You have ' + str(len(divisions)) + ' trips to take this year! \n Now, pick some destinations.')
            break
        except ValueError:
            print 'Sorry, you need to enter a number. Please try again.'
    destList =[]
    while len(destList) < len(divisions):
        newDest = raw_input('Where would you like to go? \n Hint: The options are New Orleans, Austin, Ocean City, Washington Crossing,San Franciso, Staycation!, and Athens. \n Hint: You can enter a destination more than once.\n')
        if newDest not in costDB.keys():
            print "Sorry, I don't have travel data for that location! Please try again."
        else:
            destList.append(newDest)
    print('Thanks! Now I can optimize your vacation...')
    optimizeYear(divisions,buildDestinations(destList))

### TESTS
#
## 1 test building the destination class
#OceanCity=destination('Ocean City')
#OceanCity.updateCosts([20,20,20,20,20,20,20,20,20,20,20,20],[0,0,0,0,600,0,0,0,0,0,0,0])
#print OceanCity.findBestMonth(5)
#
## 2 test optimizing the year with two destinations
#Cruise=destination('Cruise')
#Cruise.updateCosts([200,200,200,100,100,400,200,200,200,400,300,500],[80,80,80,80,80,60,80,80,80,80,80,100])
#optimizeYear([5,5],[OceanCity,Cruise])
#
## 3 test that a single destination can be visited multiple times
#optimizeYear([5,5,10],[OceanCity,OceanCity,Cruise])
#
## 4 build destination classes
#print buildDestinations(["Ocean City","San Francisco","Athens"])
#
## 5 optimize year with inputs of vacation time and city list
#optimizeYear(tripDivisions(11),buildDestinations(["Ocean City","San Francisco","Athens"]))

### TO DO LIST
# replace mock data with real data
# print the schedule in order
# improve 'optimization' - more flexibility in # days at each location
# allow user-input restrictions (ex. blackout dates, min/max trip lengths, max # trips in one month)
# incorporate weather data
# allow user-input restrictions around weather
