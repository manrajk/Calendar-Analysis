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
import time



keywords = ["phy", "math", "cas", "phil", "cs"]
startDate = datetime.date(2021, 1, 1)
endDate = datetime.date(2021,5,26)
selectFile = 'CalendarFiles/may18.ics'

temp1 = dataframeCreator(selectFile)
tik = time.perf_counter()
temp = getEventsAndTimes(temp1, keywords, startDate, endDate)
tok = time.perf_counter()
print(f"Dataframe method {tok-tik:0.4f}")



import tryAgainst

print()
tik = time.perf_counter()
temp2 = tryAgainst.getEventsAndTimes(selectFile,keywords,startDate,endDate)
tok = time.perf_counter()
print(f"Reader method {tok-tik:0.4f}")
