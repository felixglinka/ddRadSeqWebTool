import os
import shutil
from datetime import datetime

from backend.settings import CHUNKED_UPLOAD_PATH_BASE


def cleanUp():
    currentTime = datetime.now()
    currentYear = currentTime.strftime('%Y')
    currentMonth = currentTime.strftime('%m')
    currentDay = currentTime.strftime('%d')

    for dir in os.listdir(CHUNKED_UPLOAD_PATH_BASE):
        if dir != currentYear:
            shutil.rmtree(os.path.join(CHUNKED_UPLOAD_PATH_BASE, dir))

    for dir in os.listdir(os.path.join(CHUNKED_UPLOAD_PATH_BASE, currentYear)):
        if dir != currentMonth:
            shutil.rmtree(os.path.join(os.path.join(os.path.join(CHUNKED_UPLOAD_PATH_BASE, currentYear)), dir))

    for dir in os.listdir(os.path.join(os.path.join(CHUNKED_UPLOAD_PATH_BASE, currentYear), currentMonth)):
        if dir != currentDay:
            shutil.rmtree(os.path.join(os.path.join(os.path.join(CHUNKED_UPLOAD_PATH_BASE, currentYear), currentMonth), dir))