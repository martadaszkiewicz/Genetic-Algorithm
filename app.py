# app.py
from flask import Flask, request, jsonify
from flask_cors import CORS
from Genetic_Algorithm import Genetic_Algorithm
from sequence_transformation import sequence_transformation
app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

@app.route('/api/run_genetic_algorithm', methods=['POST'])
def run_genetic_algorithm():
    data = request.get_json()
    x = data['x']
    y = data['y']
    P = data['P']
    n = data['n']
    p_m = data['p_m']

    cost, sequence, time_to_process = Genetic_Algorithm(x, y, P, n, p_m)

    # converting numny arrays to Python lists using tolist() (it was necessary)
    cost = cost.tolist()
    sequence = sequence.tolist()

    x_results = sequence_transformation(sequence, x)
    y_results = sequence_transformation(sequence, y)

    
    response = {
        'cost': cost,
        'sequence': sequence,
        'time_to_process': time_to_process,
        'x_results': x_results,
        'y_results': y_results
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(port=5000)
