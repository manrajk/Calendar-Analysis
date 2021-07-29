"""
Something that have become very interesting is that when picking keywords
it is important not to pick phrases that may appear in other words

Some that I personally noticed are
The word physics has cs in it
The word  philosophy has  phy in it
"""
from functions import bubbleSort
from icalendar import Calendar
import datetime




# Setting up variables and needed data
eventsAndTime = {}
eventsAndTitles = {}
dayLongEvents = []
keywords = ["phy", "math", "cas", "phil", "cs"]
startDate = datetime.date(2021, 1, 1)
endDate = datetime.date(2021,5,26)
selectFile = 'CalendarFiles/may18.ics'

# Sorting keywords from biggest length to smallest
# This is to prevent problems described in the docString
bubbleSort(keywords)

# Opens file and sets it up for reading
g = open(selectFile,'rb')
gcal = Calendar.from_ical(g.read())

# Goes through each event
for component in gcal.walk():
    if component.name == "VEVENT":

        # Gets the important information and puts into variables
        name = str(component.get('summary')).lower()
        start = component.get('dtstart').dt
        end = component.get('dtend').dt
        date = datetime.date(component.get('dtstart').dt.year, component.get('dtstart').dt.month, component.get('dtstart').dt.day)
        time_elapsed = end-start
        
        # Checks if date is in the parameters
        if date > startDate and date < endDate:
            beenAdded = False
            
            # Checks if its all day events
            if time_elapsed.days == 1:
                dayLongEvents.append(name)
            
            # Goes through all keywords
            for keyword in keywords:

                # If keyword is found in the event name
                if keyword in name:
                    if keyword in eventsAndTime:
                        eventsAndTime[keyword] += time_elapsed
                    else:
                        eventsAndTime[keyword] = time_elapsed
                    
                    if keyword in eventsAndTitles:
                        eventsAndTitles[keyword].append(name)
                    else:
                        eventsAndTitles[keyword] = []
                        eventsAndTitles[keyword].append(name)
                    beenAdded = True
                    break
            
            # This is for events which had none of the keywords
            if not beenAdded:

                # Creates a misc category
                if "misc" in eventsAndTime:
                    eventsAndTime["misc"] += time_elapsed
                else:
                    eventsAndTime["misc"] = time_elapsed

                if "misc" in eventsAndTitles:
                    eventsAndTitles["misc"].append(name)
                else:
                    eventsAndTitles["misc"] = []
                    eventsAndTitles["misc"].append(name)


# Converts to hours
for key in eventsAndTime:
    totalSeconds = eventsAndTime[key].days * 86400 + eventsAndTime[key].seconds
    inHours = totalSeconds / 3600
    eventsAndTime[key] = inHours

g.close()