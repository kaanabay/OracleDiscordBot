from datetime import datetime


def GetDateStr(dateTime=datetime.now()):
    return dateTime.strftime('%Y%m%d%H%M%S')


def GetDateStrPretty(dateTime=datetime.now()):
    return dateTime.strftime('%d.%m.%Y %H:%M:%S')
