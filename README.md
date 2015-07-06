# vacaplanner

vacaplanner is an annual travel planner.

depending on how many vacation days you have to spend this year and which destinations you want to visit, vacaplanner will find the travel schedule that minimizes total cost.

## summary

vacaplanner.py requests information from the user on vacation allowance for the upcoming year and destinations of interest. 
considering the cost to visit each destination at different times of year, the program optimizes the user's schedule to minimize cost.
vacaplanner.py returns a proposed travel schedule.

## inputs and assumptions

vacaplanner imports travel costs from the traveldata.py file. 

traveldata.py contains **mock data** for monthly travel and lodging costs to a number of destinations.

currently, vacaplanner uses a simple rule to divide the total vacation allowance into multiple trips. the program assumes that the user will split vacation allowance into full-week trips and three-day weekends. first, the number of full-week trips is maximized; any leftover days are used on three-day weekends.

note: the "destination" class in vacaplanner.py includes attributes for weather data. these attributes are not yet used. weather data will eventually be incorporated to include additional user preferences: ex. avoid destinations at overly hot/cold times of year, or avoid rainy seasons.
