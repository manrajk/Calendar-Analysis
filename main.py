"""
Something that have become very interesting is that when picking keywords
it is important not to pick phrases that may appear in other words

Some that I personally noticed are
The word physics has cs in it
The word  philosophy has  phy in it
"""
from SelectionData import SelectionData
import datetime
import pandas as pd
import time




keywords = ["phy", "math", "cas", "phil", "cs"]
startDate = datetime.date(2021, 1, 1)
endDate = datetime.date(2021,5,18)
selectFile = 'CalendarFiles/may18.ics'

tik = time.perf_counter()
dataDF = SelectionData(selectFile)
tok = time.perf_counter()
print(f"{tok-tik:0.4f}")
    


 
