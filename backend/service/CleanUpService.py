from datetime import datetime

def cleanUp():
    currentTime = datetime.now()
    currentYear = currentTime.year
    currentMonth = currentTime.month
    currentDay = currentTime.day

    print(currentYear, currentMonth, currentDay)