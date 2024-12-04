#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  4 15:18:13 2024

@author: 21408644
"""

from flask import Flask, jsonify, request

app = Flask(__name__)

nourrir: int=0

# Define a Python function
def nourrir(nombre:int) -> int:
    nourrir: int += nombre
    return nourrir

# Create an endpoint that calls the Python function
@app.route('/nombre', methods=['GET'])
def add_numbers():
    # Get query parameters
    x = int(request.args.get('x'))
    y = int(request.args.get('y'))

    # Call the Python function
    result = my_python_function(x, y)
    
    # Return the result as JSON
    return jsonify({"result": result})

if __name__ == '__main__':
    app.run(debug=True)
