import json
import datetime
import pytz
import os
import utils as utils


## Function to query all configured devices
def getStoredDevices():
    response = {}
    jsonResponse = {}
    devices = []
    deviceEntry = {}

    ## @TODO: add try catch
    with open('resources/configured_devices.json') as jsonFile:
        data = json.load(jsonFile)

        for device in data['devices']:
            deviceEntry = {
                "deviceName" : device['name'],
                "latitude"   : device['latitude'],
                "longitude"  : device['longitude']
            }
            devices.append(deviceEntry)

        # Build json response
        response = { "devices" : devices }
        jsonResponse = json.dumps(response) 

    return jsonResponse
 

## Function to query summary data for a configured device
def getSummaryData(deviceName):
    response = {}
    jsonResponse = {}
    samples = []
    dailySample = {}
    files = []

    startingDate = datetime.datetime.strptime(utils.daysAgo(16), "%Y-%m-%d %H:%M:%S")
    startingDate = int(startingDate.replace(tzinfo=pytz.utc).timestamp())

    directory = os.fsencode("resources/samples")

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.startswith(deviceName):
            if int(filename.split("_")[1]) >= startingDate:
                files.append("resources/samples/" + filename)
        else:
            continue

    if not file:
        return jsonResponse

    ## Sort list in descending order
    files.sort(reverse=True)
    
    ## @TODO: add try catch
    for file in files:
        with open(file) as jsonFile:
            data = json.load(jsonFile)
            dailySample = {
                "time"      : data["day"],
                "avgTemp"   : data["avgDailyTemp"],
                "avgCo2"    : data["avgDailyCo2"],
                "avgRad"    : data["avgDailyRad"],
                "avgO3"     : data["avgDailyO3"],
                "avgNo2"    : data["avgDailyNo2"],
                "avgCo"     : data["avgDailyCo"],
                "avgVoc"    : data["avgDailyVoc"],
                "avgPm2_5"  : data["avgDailyPm2_5"],
                "avgPm10"   : data["avgDailyPm10"],
                "avgDs18"   : data["avgDailyDs18"]
            }
            samples.append(dailySample.copy())

    response = { "samples" : samples }
    jsonResponse = json.dumps(response) 

    return jsonResponse


def getDeviceData(deviceName, startTime, endTime):
    response = {}
    jsonResponse = {}
    samples = []
    dailySample = {}
    reduceDataSet = False
    samplesThreshold = 20
    entitiesCount = 0
    files = []

    requestedDays = utils.daysBetween(startTime, endTime)

    # Adding time to requested days in order to correctly query the dbs
    startTime = datetime.datetime.strptime(startTime + " 00:00:00", "%Y-%m-%d %H:%M:%S")
    endTime = datetime.datetime.strptime(endTime + " 23:59:59", "%Y-%m-%d %H:%M:%S")
    startTime = int(startTime.replace(tzinfo=pytz.utc).timestamp())
    endTime = int(endTime.replace(tzinfo=pytz.utc).timestamp())

    directory = os.fsencode("resources/samples")

    for file in os.listdir(directory):
        filename = os.fsdecode(file)
        if filename.startswith(deviceName):
            fileDate = int(filename.split("_")[1])
            if fileDate >= startTime and fileDate <= endTime:
                files.append("resources/samples/" + filename)
        else:
            continue

    if not file:
        return jsonResponse

    # If the dataset need to be shorter (a lot of data has been requested)
    if requestedDays >= samplesThreshold and len(file) >= samplesThreshold:
        reduceDataSet = True

    ## Sort list in descending order
    files.sort()

    ## @TODO: add try catch
    for file in files:
        with open(file) as jsonFile:
            data = json.load(jsonFile)
            if reduceDataSet:
                dailySample = {
                    "time"          : data["day"],
                    "missingData"   : "false",
                    "avgTemp"       : data["avgDailyTemp"],
                    "avgCo2"        : data["avgDailyCo2"],
                    "avgRad"        : data["avgDailyRad"],
                    "avgO3"         : data["avgDailyO3"],
                    "avgNo2"        : data["avgDailyNo2"],
                    "avgCo"         : data["avgDailyCo"],
                    "avgVoc"        : data["avgDailyVoc"],
                    "avgPm2_5"      : data["avgDailyPm2_5"],
                    "avgPm10"       : data["avgDailyPm10"],
                    "avgDs18"       : data["avgDailyDs18"]
                }
                samples.append(dailySample.copy())
            else:
                samples += data["data"]
    
    # Build the response and converting it to jsons
    response = { "samples" : samples }
    jsonResponse = json.dumps(response) 

    return jsonResponse