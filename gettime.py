import datetime
import pytz

def thetime():
    timezone = pytz.timezone('Asia/Kuala_Lumpur')
    currentTime = datetime.datetime.now(tz=timezone) # To get the current time in particular timezone

    return currentTime