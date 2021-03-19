from datetime import datetime


def GetDateStr(dateTime):
    return dateTime.strftime('%Y%m%d%H%M%S')


def GetDateStrPretty(dateTime):
    return dateTime.strftime('%d.%m.%Y %H:%M:%S')
