from os import walk
from icalendar import Calendar
import datetime
import pandas as pd



def dataframeCreator(selectFile):
    # Opens file and sets it up for reading
    g = open(selectFile,'rb')
    gcal = Calendar.from_ical(g.read())

    # Creates a dateframe with relevant data from ics file
    df = pd.DataFrame(columns=['Name','Start Time','End Time','Date','Time Elapsed'])
    for component in gcal.walk():
        if component.name == "VEVENT":

            # Gets the important information and puts into variables
            name = str(component.get('summary')).lower()
            start = component.get('dtstart').dt
            end = component.get('dtend').dt
            date = datetime.date(component.get('dtstart').dt.year, component.get('dtstart').dt.month, component.get('dtstart').dt.day)
            time_elapsed = end-start

            d = {'Name':name, 'Start Time':start, 'End Time':end, 'Date':date, 'Time Elapsed':time_elapsed}
            df = df.append(d, ignore_index=True)

    g.close()
    return df


def bubbleSort(arr):
    '''
    Sorted from largest length to smallest length
    '''

    n = len(arr)

    for i in range(0,n-1):
        for j in range(n-i-1):
            if len(arr[j]) < len(arr[j+1]):
                arr[j], arr[j+1] = arr[j+1], arr[j]


def getEventsAndTimes(df, keywords, startDate, endDate=datetime.date.today()):
    '''
    This will return 3 things: eventsAndTime, eventsAndTitles and dayLongEvents
    The first two are dictionaries and the last is a list
    '''

    # Setting up variables and needed data
    eventsAndTime = {}
    eventsAndTitles = {}
    dayLongEvents = []

    # Sorting keywords from biggest length to smallest
    # This is to prevent problems described in the docString
    bubbleSort(keywords)

    # Opens file and sets it up for reading
    df = df[ (df['Date'] > startDate) & (df['Date'] < endDate) ]
    
    for d in df.to_dict('records'):

        beenAdded = False
        name = d['Name']
        time_elapsed = d['Time Elapsed']
        
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

    return eventsAndTime, eventsAndTitles, dayLongEvents