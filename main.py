"""
Something that have become very interesting is that when picking keywords
it is important not to pick phrases that may appear in other words

Some that I personally noticed are
The word physics has cs in it
The word  philosophy has  phy in it
"""
from functions import *
import datetime
import pandas as pd



keywords = ["phy", "math", "cas", "phil", "cs"]
startDate = datetime.date(2021, 1, 1)
endDate = datetime.date(2021,5,26)
selectFile = 'CalendarFiles/may18.ics'

temp = getEventsAndTimes(selectFile, keywords, startDate, endDate)