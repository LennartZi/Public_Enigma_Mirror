from flask import Flask, jsonify, request
from flask import current_app as app
import yaml


@app.route("/config")
def config():
    with open("/etc/enigma.yaml", "r") as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


# Endpoint for getting the available variants
@app.route('/variants', methods=['GET'])
def get_variants():
    variants = ['A', 'B', 'C']
    return jsonify(variants)


# Endpoint for setting the current variant
@app.route('/variant', methods=['PUT'])
def set_variant():
    variant = request.headers.get('variant')
    response = app.make_response('')
    response.headers['Set-Cookie'] = f'variant={variant}'
    return response


# Endpoint for getting the available rotors
@app.route('/rotors', methods=['GET'])
def get_rotors():
    variant_cookie = request.cookies.get('variant')
    if not variant_cookie:
        return 'Variant cookie not set', 400
    rotors = [
        {'name': 'I', 'entry': True, 'reflector': False},
        {'name': 'II', 'entry': True, 'reflector': False},
        {'name': 'III', 'entry': True, 'reflector': False},
    ]
    return jsonify(rotors)


# Endpoint for setting the current rotor for a given rotor number
@app.route('/rotor/<int:rotornr>', methods=['PUT'])
def set_rotor(rotornr):
    variant_cookie = request.cookies.get('variant')
    if not variant_cookie:
        return 'Variant cookie not set', 400
    rotor = request.headers.get('rotor')
    response = app.make_response('')
    response.headers['Set-Cookie'] = f'rotors={{{rotornr}: {rotor}}}'
    return response


# Endpoint for getting/setting the starting position for a given rotor number
@app.route('/rotor/<int:rotornr>/position', methods=['GET', 'PUT'])
def rotor_position(rotornr):
    if request.method == 'GET':
        return jsonify(1)
    elif request.method == 'PUT':
        position = request.headers.get('position')
        response = app.make_response('')
        response.headers['Set-Cookie'] = f'position={{{rotornr}: {position}}}'
        return response


# Endpoint for encrypting a letter
@app.route('/encrypt', methods=['PUT'])
def encrypt_letter():
    letter = request.headers.get('letter')
    response = app.make_response(letter)
    response.headers['Set-Cookie'] = 'history=abc ; position={0: 26, 1: 12, 2:1}'
    return response
