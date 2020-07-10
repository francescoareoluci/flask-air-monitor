from flask import Flask
from flask import request
from flask_cors import CORS, cross_origin
import utils as utils
import api_handlers as handlers

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/api/registered-devices')
@cross_origin()
def handleConfiguredDevices():
    jsonResult = handlers.getStoredDevices()

    return jsonResult


@app.route('/api/summary-data')
@cross_origin()
def handleSummaryData():
    device = request.args.get('device-name')

    if not device or device == "" or not device.isalnum():
        abort(400)
        return

    jsonResult = handlers.getSummaryData(device)

    return jsonResult


@app.route('/api/device-data')
@cross_origin()
def handleDeviceData():
    device = request.args.get('device-name')
    startDate = request.args.get('from')
    endDate = request.args.get('to')

    if not device or device == "" or not device.isalnum():
        abort(400)
        return

    if not startDate or startDate == "" or not utils.dateValidation(startDate):
        abort(400)
        return

    if not endDate or endDate == "" or not utils.dateValidation(endDate):
        abort(400)
        return

    jsonResult = handlers.getDeviceData(device, startDate, endDate)

    return jsonResult