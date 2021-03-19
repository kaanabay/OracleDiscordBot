import os
from datetime import datetime
from dotenv import load_dotenv
import GeneralUtils

load_dotenv()
LOGFILENAME = os.getenv('LOGFILENAME')


def Log(message, user='GHOST'):
    dateStr = GeneralUtils.GetDateStrPretty(datetime.now())

    with open(LOGFILENAME, 'a') as file:
        file.write(' - '.join((dateStr, user, message)))
        file.write('\n')
