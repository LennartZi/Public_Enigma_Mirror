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
    with open("/etc/enigma.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            variants = list(data['variants'].keys())
            return jsonify(variants)
        except yaml.YAMLError as exc:
            return 'Error loading variants', 500


# Endpoint for setting the current variant
@app.route("/variant", methods=["GET", "PUT"])
def handle_variant():
    if request.method == "GET":
        variant_cookie = request.cookies.get("variant")
        if variant_cookie:
            return jsonify(variant_cookie)
        else:
            return "Variant cookie not set", 400
    elif request.method == "PUT":
        variant = request.headers.get("variant")
        response = app.make_response("")
        set_cookie(response, "variant", variant)
        return response


# Endpoint for getting the available rotors
@app.route('/rotors', methods=['GET'])
def get_rotors():
    variant_cookie = request.cookies.get('variant')
    if not variant_cookie:
        return 'Variant cookie not set', 400

    with open("/etc/enigma.yaml", "r") as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)

    variant = data['variants'].get(variant_cookie)
    if not variant:
        return 'Variant not found in YAML', 400

    rotors = []
    rotor_info = variant['rotors']
    available_rotors = rotor_info.keys()
    for rotor_name, rotor_data in rotor_info.items():
        if rotor_name == 'installable':
            continue
        rotor = {
            'name': rotor_name,
            'entry': False,
            'reflector': False,
            'substitution': rotor_data['substitution'],
            'turnover': rotor_data['turnover']
        }
        rotors.append(rotor)

    return jsonify(rotors)


# Endpoint for setting the current rotor for a given rotor number
@app.route('/rotor/<int:rotornr>', methods=['GET', 'PUT'])
def set_rotor(rotornr):
    variant_cookie = request.cookies.get('variant')
    if not variant_cookie:
        return 'Variant cookie not set', 400

    rotors_cookie = request.cookies.get('rotors')
    rotors = json.loads(rotors_cookie) if rotors_cookie else [None, None, None]

    if request.method == 'GET':
        rotor = rotors[rotornr]
        response_data = {'rotor': rotor} if rotor is not None else {'message': 'No rotor selected at this position'}
        return jsonify(response_data)
    elif request.method == 'PUT':
        rotor = request.headers.get('rotor')

        with open("/etc/enigma.yaml", "r") as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)

        variant = data['variants'].get(variant_cookie)
        if not variant:
            return 'Variant not found in YAML', 400

        valid_rotors = variant['rotors'].keys()
        if rotor not in valid_rotors:
            return 'Invalid rotor for the selected variant', 400

        rotors[rotornr] = rotor

        response = app.make_response('')
        set_cookie(response, "rotors", json.dumps(rotors))
        return response


# Endpoint for getting/setting the starting position for a given rotor number
@app.route('/rotor/<int:rotornr>/position', methods=['GET', 'PUT'])
def rotor_position(rotornr):
    if request.method == 'GET':
        positions = request.cookies.get("positions") or '["A", "A", "A"]'
        positions = json.loads(positions)
        position = positions[rotornr]
        string = "Rotor " + str(rotornr) + " position"
        return jsonify({string: position})
    elif request.method == 'PUT':
        positions = request.cookies.get("positions") or '["A", "A", "A"]'
        positions = json.loads(positions)
        position = request.headers.get("position")
        positions[rotornr] = position
        response = app.make_response('')
        set_cookie(response, "positions", json.dumps(positions))
        return response


# Endpoint to retrieve the input history and regular history
@app.route("/history", methods=['GET'])
def get_history():
    input_history = request.cookies.get("input_history") or ""
    history = request.cookies.get("history") or ""
    return jsonify({"input_history": input_history, "history": history})


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
        input_letter = letter
        letter = enigma_b.encode_letter(letter)
        positions = enigma_b.rotor_positions

        response = jsonify(letter)
        set_cookie(response, "positions", json.dumps(positions))

        # Saves input-history in cookie
        input_history = request.cookies.get("input_history") or str()
        input_history += input_letter
        input_history = input_history[-140:]
        set_cookie(response, "input_history", input_history)

        # Saves history in cookie
        history = request.cookies.get("history") or str()
        history += letter
        history = history[-140:]
        set_cookie(response, "history", history)

        return response
