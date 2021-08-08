from logging import error
from typing import Counter
from numpy.core.numeric import full
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from calendarParser import getEventsAndTimes


class SelectionData:

    def __init__(self,fullDF,keywords, startDate,endDate,days=0,weeks=0):   
        """
        End Date is not inclusive
        """
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
            eventsAndTimes, eventsAndTitles, dayLongEvents = getEventsAndTimes(fullDF, keywords, pointer1, pointer2)
            fullDictionary[counter] = eventsAndTimes

            # Creates time label for segment and moves pointers
            columnNames.append( labelMaker(pointer1, pointer2) )
            pointer1 = pointer2
            pointer2 += delta
            counter += 1

        # In the end the weeks/days do not match exactly
        if pointer2 == endDate:
            pass
        elif pointer2 > endDate:
            eventsAndTimes, eventsAndTitles, dayLongEvents = getEventsAndTimes(fullDF, keywords, pointer1, endDate)
            fullDictionary[counter] = eventsAndTimes
            columnNames.append( labelMaker(pointer1, endDate) )
        else:
            print('Something strange is happening')

        # Putting together all of the columns into place
        finalDF = pd.DataFrame.from_dict(fullDictionary)
        finalDF.columns = columnNames

        self.segmentedDF = finalDF
        self.keywords = keywords


    def graphing(self):
        sns.set_theme(style='darkgrid')
        
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