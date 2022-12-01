"""
This programs connects the MESA python code as an API in
order to be retrieved by Unity

Aleny Sofia Arévalo Magdaleno |  A01751272
Luis Humberto Romero Pérez | A01752789
Valeria Martínez Silva | A01752167
Pablo González de la Parra | A01745096

Created: 25 / 11 / 2022
"""

from flask import Flask, request, jsonify
from model import *

initial_cars = 10
cars_every = 5
cityModel = None
currentStep = 0
maxSteps = 0


app = Flask("City")


@app.route('/', methods=['POST', 'GET'])
def helloWorld():
    if request.method == 'GET':
        return jsonify({"message": "Connection with server was successful!"})


@app.route('/init', methods=['POST', 'GET'])
def initModel():
    global currentStep, cityModel, initial_cars, cars_every

    if request.method == 'POST':
        initial_cars = int(request.form.get('InitialCars'))
        cars_every = int(request.form.get('CarsEvery'))
        currentStep = 0

        cityModel = CityModel(initial_cars, cars_every)

        return jsonify({"message": "Parameters received, model initiated."})


@app.route('/getCars', methods=['GET'])
def getCars():
    global cityModel

    if request.method == 'GET':
        carPositions = [{"id": str(obj.unique_id),
                         "x": x, "y": 0, "z": z,
                         "reached_destination": obj.reached_destination}
                        for (a, x, z) in cityModel.grid.coord_iter()
                        for obj in a if isinstance(obj, Car)]
        return jsonify({'positions': carPositions})


@app.route('/getLights', methods=['GET'])
def getTrafficLight():
    global cityModel

    if request.method == 'GET':
        carPositions = [{"id": str(obj.unique_id),
                         "x": x, "y": 1.5, "z": z,
                         "state": obj.state}
                        for (a, x, z) in cityModel.grid.coord_iter()
                        for obj in a if isinstance(obj, Traffic_Light)]
        return jsonify({'positions': carPositions})


@app.route('/update', methods=['GET'])
def updateModel():
    global currentStep, cityModel
    if request.method == 'GET':
        cityModel.step()
        currentStep += 1
        return jsonify({'message': f'Model updated to step {currentStep}.',
                        'currentStep': currentStep})


if __name__ == '__main__':
    app.run(host="localhost", port=8585, debug=True)
