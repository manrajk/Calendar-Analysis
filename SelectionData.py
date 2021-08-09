from numpy.lib.utils import info
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from icalendar import Calendar
from tools import bubbleSort


class SelectionData:
    def __init__(self,selectFile):
        # Opens file and sets it up for reading
        g = open(selectFile,'rb')
        gcal = Calendar.from_ical(g.read())

        # Creates a dateframe with relevant data from ics file
        builtDictionary = {}
        counter = 0

        for component in gcal.walk():
            if component.name == "VEVENT":

                # Gets the important information and puts into variables
                name = str(component.get('summary')).lower()
                start = component.get('dtstart').dt
                end = component.get('dtend').dt
                date = datetime.date(component.get('dtstart').dt.year, component.get('dtstart').dt.month, component.get('dtstart').dt.day)
                time_elapsed = end-start

                d = {'Name':name, 'Start Time':start, 'End Time':end, 'Date':date, 'Time Elapsed':time_elapsed}
                builtDictionary[counter] = d
                counter += 1

        g.close()
        df =  pd.DataFrame.from_dict(builtDictionary,'index')

        # Sorting it by date
        df = df.sort_values('Date')

        # Sets up attributes
        self.rawCalendarDF = df
        self.segmentedDF = None


    def getEventsAndTimes(self, keywords, startDate, endDate=datetime.date.today()):

        # Setting up variables and needed data
        eventsAndTime = {}
        eventsAndTitles = {}
        dayLongEvents = []

        # Sorting keywords from biggest length to smallest
        # This is to prevent problems described in the docString
        bubbleSort(keywords)
        keywords = list((map(lambda x: x.lower(), keywords)))

        # Opens file and sets it up for reading
        df = self.rawCalendarDF[ (self.rawCalendarDF['Date'] >= startDate) & (self.rawCalendarDF['Date'] < endDate) ]
        
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


    def calendarSegmenter(self,keywords, startDate,endDate,days=0,weeks=0):   
        """
        End Date is not inclusive
        """

        if days == 0 and weeks == 0:
            delta = endDate - startDate
            delta = datetime.timedelta(days=delta.days)
        else:
            delta = datetime.timedelta(days=days, weeks=weeks)

        pointer1 = startDate
        pointer2 = pointer1 + delta
        fullDictionary = {}
        counter = 0
        columnNames = []

        # Lambda that checks if this is within the same year
        labelMaker = lambda p1, p2: f'{p1.month}/{p1.day} to {p2.month}/{p2.day}' if startDate.year == endDate.year else f'{p1.month}/{p1.day}/{p1.year} to {p2.month}/{p2.day}/{p2.year}'

        # Moves pointer throughout the start to endDates in segments determined from arguments
        while endDate >= pointer2:
            # Gets Data for segment
            eventsAndTimes, eventsAndTitles, dayLongEvents = self.getEventsAndTimes(keywords, pointer1, pointer2)
            fullDictionary[counter] = eventsAndTimes

            # Creates time label for segment and moves pointers
            columnNames.append( labelMaker(pointer1, pointer2) )
            pointer1 = pointer2
            pointer2 += delta
            counter += 1

        # In the end the weeks/days do not match exactly
        if pointer2 == endDate:
            pass
        elif pointer2 > endDate and pointer1 != endDate:
            eventsAndTimes, eventsAndTitles, dayLongEvents = self.getEventsAndTimes(keywords, pointer1, endDate)
            fullDictionary[counter] = eventsAndTimes
            columnNames.append( labelMaker(pointer1, endDate) )

        # Putting together all of the columns into place
        finalDF = pd.DataFrame.from_dict(fullDictionary)
        finalDF.columns = columnNames

        self.segmentedDF = finalDF


    def graphing(self):
        sns.set_theme(style='darkgrid')

        if self.segmentedDF is None:
            return 'Need to select Segment First'
        
        graphingDF = self.segmentedDF.T
        foundKeywords = graphingDF.columns.to_series()
        foundKeywords = foundKeywords.drop('misc', errors='ignore')


        if len(foundKeywords) > 0:
            numberingSeries = pd.Series(dtype='float64')
            labelSeries = pd.Series()

            for x in foundKeywords:
                numberingSeries = numberingSeries.append( graphingDF[x], ignore_index=True )
                labelSeries = labelSeries.append( pd.Series([x for i in range(len( graphingDF.index ))]), ignore_index=True )

            reorganizedDF = pd.DataFrame(columns=['Labels', 'Numbering', 'Time'])
            reorganizedDF['Time'] = pd.concat( [graphingDF.index.to_series()]*len(foundKeywords), ignore_index=True )
            reorganizedDF['Numbering'] = numberingSeries
            reorganizedDF['Labels'] = labelSeries
            ax = sns.barplot(x='Time', y='Numbering', hue='Labels', data=reorganizedDF)
            ax.set_xticklabels(graphingDF.index, rotation=45, ha='right')

            plt.tight_layout()
            plt.show()
        else:
            return 'No matching Keywords'

    
    def keywordStreakFinder(self,keywords,firstDate=None):

        # DataFrame with only 'Name' and 'Date'
        nameAndDatesDF = self.rawCalendarDF.drop(['Start Time','End Time','Time Elapsed'],axis=1)

        # Making range of dates
        if firstDate == None:
            firstDate = nameAndDatesDF.iloc[0]['Date']
        end = datetime.date.today()
        dateList = [firstDate + datetime.timedelta(days=x) for x in range( (end - firstDate).days )]

        # Keep track of what has a steak based on keywords
        '''
        streaks
        name,startDate,length of streak

        unactiveStreaks
        name,startDate,list of length of streak
        '''

        bubbleSort(keywords)
        keywords = list((map(lambda x: x.lower(), keywords)))

        streaks = {}
        unactiveStreaks = {}

        # Parse
        for date in dateList:
            dfAtDate = nameAndDatesDF[ nameAndDatesDF['Date'] == date ]
            '''
            
            Check if dfAtDate is empty
                if no make needed changes
                    go through dfAtDate events
                        go through keywords
                            make temp dict with new streaks
                            if keyword is in events 
                                check if it is in streaks 
                                if it is add that info and the new tally to the temp
                                else add to temp
                                break


                if yes clear streaks

            '''

        

    
    # def autoStreakFinder(self,firstDate=None):

    #     # DataFrame with only 'Name' and 'Date'
    #     nameAndDatesDF = self.rawCalendarDF.drop(['Start Time','End Time','Time Elapsed'],axis=1)

    #     # Making range of dates
    #     if firstDate == None:
    #         firstDate = nameAndDatesDF.iloc[0]['Date']
    #     end = datetime.date.today()
    #     dateList = [firstDate + datetime.timedelta(days=x) for x in range( (end - firstDate).days )]

    #     # Keep track of what has a steak based on same 'Name' in DataFrame
    #     streaks = {}
    #     unactiveStreaks = {}

    #     # Parse

        