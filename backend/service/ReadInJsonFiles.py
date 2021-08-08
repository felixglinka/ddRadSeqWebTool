import json
import os

from backend.settings import STATIC_ROOT


def readInPopoverTexts():

    with open(os.path.join(STATIC_ROOT, 'json/popoverContent.json'), encoding='utf-8-sig') as popoverContent:
        readPopoverContent = popoverContent.read()
        popoverJson = json.loads(readPopoverContent)

    return popoverJson

def readInBeginnerInformationTexts():

    with open(os.path.join(STATIC_ROOT, 'json/beginnerInformation.json'), encoding='utf-8-sig') as beginnerInformation:
        readBeginnerInformation = beginnerInformation.read()
        beginnerInformationJson = json.loads(readBeginnerInformation)

    return beginnerInformationJson