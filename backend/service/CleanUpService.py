import os
from datetime import datetime

from backend.settings import CHUNKED_UPLOAD_PATH_BASE


def cleanUp():
    currentTime = datetime.now()
    currentYear = currentTime.strftime('%Y')
    currentMonth = currentTime.strftime('%m')
    currentDay = currentTime.strftime('%d')

    for dir in os.listdir(CHUNKED_UPLOAD_PATH_BASE):
        if dir != currentYear:
            os.remove(os.path.join(CHUNKED_UPLOAD_PATH_BASE, dir))

    for dir in os.listdir(os.path.join(CHUNKED_UPLOAD_PATH_BASE, currentYear)):
        if dir != currentMonth:
            os.remove(os.path.join(CHUNKED_UPLOAD_PATH_BASE, dir))

    for dir in os.listdir(os.path.join(os.path.join(CHUNKED_UPLOAD_PATH_BASE, currentYear), currentMonth)):
        if dir != currentDay:
            os.remove(os.path.join(CHUNKED_UPLOAD_PATH_BASE, dir))