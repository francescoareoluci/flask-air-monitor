import datetime

## Util function to evaluate date difference
def daysBetween(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


## Util function to evaluate if requested date
# format is corrects
def dateValidation(dateStr):
    dateFormat = "%Y-%m-%d"

    try:
      datetime.datetime.strptime(dateStr, dateFormat)
      return True
    except ValueError:
      return False


## Util function to evaluate date difference
def daysBetween(d1, d2):
    d1 = datetime.datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.datetime.strptime(d2, "%Y-%m-%d")
    return abs((d2 - d1).days)


## Util function to get a date daysNumber days
# before today
def daysAgo(daysNumber):
    today = datetime.date.today()
    lastWeek = today - datetime.timedelta(days = daysNumber)
    startingDate = lastWeek.strftime("%Y-%m-%d") + " 00:00:00"
    return startingDate