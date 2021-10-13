"""
Something that have become very interesting is that when picking keywords
it is important not to pick phrases that may appear in other words

Some that I personally noticed are
The word physics has cs in it
The word  philosophy has  phy in it
"""
from SelectionData import CalendarData
import datetime
import time


def main():
    # Example code
    keywords = ["221", "360", "ArtH", "Geo", "270"]
    startDate = datetime.date(2021, 8, 1)
    endDate = datetime.date.today()
    selectFilePath = 'CalendarFiles/oct13.ics'

    # Creates CalendarData object using file path
    dataDF = CalendarData(selectFilePath)

    # See raw data from the calendar
    print(dataDF.rawCalendarDF)

    # Seperates and filters raw calendar data
    dataDF.calendarSegmenter(keywords, startDate, endDate, weeks=1)

    # Display graph
    dataDF.graphing()

    # See event streaks
    print(dataDF.keywordStreakFinder(keywords,startDate))




if __name__ == '__main__':
    main()


 
