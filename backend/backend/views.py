from flask import Flask, jsonify, request, json
from flask import current_app as app
from threading import Lock
from .enigma import Enigma
import yaml


def set_cookie(response, key: str, value):
    response.set_cookie(key, str(value), max_age=3600*24*365, path="/", samesite="Lax")

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
        positions = request.cookies.get("positions") or '["A", "A", "A"]'

        positions = json.loads(positions)
        first_position = positions[0]
        second_position = positions[1]
        third_position = positions[2]

        enigma_b = Enigma(rotor_I, rotor_II, rotor_III, first_position, second_position, third_position, ukw_b, "Q", "E",
                          "V")

        data = request.get_json()
        letter = data.get('letter')
        letter = enigma_b.encode_letter(letter)

        # TODO: change to get_rotor_position. Check that the order is consistent with the previous implementation
        positions = enigma_b.rotor_positions

        response = jsonify(letter)
        set_cookie(response, "positions", json.dumps(positions))

        history = request.cookies.get("history") or str()
        history += letter
        history = history[-140:]
        set_cookie(response, "history", history)

        return response
