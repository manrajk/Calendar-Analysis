from typing import Counter
from numpy.core.numeric import full
import pandas as pd
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from calendarParser import getEventsAndTimes


def getSectionData(fullDF,keywords, startDate,endDate,days=0,weeks=0):
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


    # Moves pointer throughout the start to endDates
    while endDate >= pointer2:
        
        eventsAndTimes, eventsAndTitles, dayLongEvents = getEventsAndTimes(fullDF, keywords, pointer1, pointer2)
        fullDictionary[counter] = eventsAndTimes

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
    finalDF = pd.DataFrame.from_dict(fullDictionary, 'columns')
    finalDF.columns = columnNames

    graphing(finalDF, keywords)
    return finalDF

    
def graphing(df, keywords):
    sns.set_theme(style='darkgrid')
    ax = None
    for keyword in keywords:
        ax = sns.relplot(x=df.columns, y=df.loc[keyword], kind='line')

    ax.set_xticklabels(df.columns, rotation=45, ha='right')


    plt.tight_layout()
    plt.show()
