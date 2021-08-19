import json
import os

from backend.settings import STATIC_ROOT


def readInPopoverTexts():

    with open(os.path.join(STATIC_ROOT, 'json/popoverContent.json'), encoding='utf-8-sig') as popoverContent:
        readPopoverContent = popoverContent.read()
        popoverJson = json.loads(readPopoverContent)

    return popoverJson

def readInInformationTexts():

    with open(os.path.join(STATIC_ROOT, 'json/beginnerInformation.json'), encoding='utf-8-sig') as informationText:
        readInformation = informationText.read()
        informationJson = json.loads(readInformation)

    return informationJson