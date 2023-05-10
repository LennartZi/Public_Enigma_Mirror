from flask import Flask, jsonify, request, json
from flask import current_app as app
from threading import Lock
from .enigma import Enigma
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

single_request = Lock()
# Endpoint for encrypting a letter
@app.route('/encrypt', methods=['PUT'])
def encrypt_letter():
    ukw_b = ['Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O', 'K', 'M', 'I', 'E', 'B',
             'F', 'Z', 'C', 'W', 'V', 'J', 'A', 'T']

    rotor_I = ['E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O', 'W', 'Y', 'H', 'X', 'U', 'S', 'P', 'A',
               'I', 'B', 'R', 'C', 'J']

    rotor_II = ['A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W', 'T', 'M', 'C', 'Q', 'G', 'Z', 'N', 'P',
                'Y', 'F', 'V', 'O', 'E']

    rotor_III = ['B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V', 'Z', 'N', 'Y', 'E', 'I', 'W', 'G', 'A',
                 'K', 'M', 'U', 'S', 'Q', 'O']

    if single_request.locked():
        return str(), 423

    with single_request:
        positions = request.cookies.get("positions")

        if positions:
            positions = json.loads(positions)
            first_position = positions[0]
            second_position = positions[1]
            third_position = positions[2]
        else:
            first_position = "A"
            second_position = "A"
            third_position = "A"

        enigma_b = Enigma(rotor_I, rotor_II, rotor_III, first_position, second_position, third_position, ukw_b, "Q", "E",
                          "V")

        letter = request.headers.get('letter')
        letter = enigma_b.encode_letter(letter)
        positions = enigma_b.rotor_positions

        print(positions)

        response = app.make_response(letter)
        response.set_cookie("positions", f'{{0: "{positions[0]}", 1: "{positions[1]}", 2: "{positions[2]}"}}')

        return response
