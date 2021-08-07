"""
Something that have become very interesting is that when picking keywords
it is important not to pick phrases that may appear in other words

Some that I personally noticed are
The word physics has cs in it
The word  philosophy has  phy in it
"""
from calendarParser import *
import datetime
import pandas as pd
from modes import *



def main():
    keywords = ["phy", "math", "cas", "phil", "cs"]
    startDate = datetime.date(2021, 1, 1)
    endDate = datetime.date(2021,5,18)
    selectFile = 'CalendarFiles/may18.ics'


    completeDataframe = dataframeCreator(selectFile)
    eventsAndTimes, eventsAndTitles, dayLongEvents = getEventsAndTimes(completeDataframe, keywords, startDate, endDate)

    neDF, graphDF = getSectionData(completeDataframe, keywords, startDate, endDate, weeks=1)
    return neDF, graphDF


if __name__ == '__main__':
    x, y= main()
    
