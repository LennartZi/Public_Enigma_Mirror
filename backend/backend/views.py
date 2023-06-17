from flask import Flask, jsonify, request, json
from flask import current_app as app
from threading import Lock
from .enigma import Enigma
import yaml
import ast


def set_cookie(response, key: str, value):
    response.set_cookie(key, str(value), max_age=3600 * 24 * 365, path="/", samesite="Lax")


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
            return jsonify("Variant cookie not set", 400)
    elif request.method == "PUT":
        variant = request.get_json()["variant"]
        response = app.make_response(jsonify("Variant " + variant + " set!"))
        set_cookie(response, "variant", variant)
        return response


@app.route('/rotors/installable', methods=['GET'])
def get_installable_rotors():
    variant_cookie = request.cookies.get('variant')
    if not variant_cookie:
        return 'Variant cookie not set', 400

    with open("/etc/enigma.yaml", "r") as stream:
        try:
            data = yaml.safe_load(stream)
            variant_rotors = data['variants'][variant_cookie]['rotors']
            return jsonify(variant_rotors['installable'])
        except yaml.YAMLError as exc:
            return 'Error loading variants', 500


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
        return jsonify('Variant not found in YAML', 400)

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
        return jsonify('Variant cookie not set', 400)

    rotors_cookie = request.cookies.get('rotors')
    rotors = json.loads(rotors_cookie) if rotors_cookie else [None, None, None]

    if request.method == 'GET':
        rotor = rotors[rotornr]
        response_data = {'rotor': rotor} if rotor is not None else ('Variant cookie not set', 400)
        return jsonify(response_data)
    elif request.method == 'PUT':
        rotor = request.get_json()['rotor']

        with open("/etc/enigma.yaml", "r") as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)

        variant = data['variants'].get(variant_cookie)
        if not variant:
            return 'Variant not found in YAML', 400

        valid_rotors = variant['rotors'].keys()
        if rotor not in valid_rotors and rotor is not None:
            return 'Invalid rotor for the selected variant', 400

        rotors[rotornr] = rotor

        response = app.make_response(jsonify("Rotor " + str(rotor) + " set on position " + str(rotornr)))
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
        position = request.get_json()["position"]
        positions[rotornr] = position
        rotors = request.cookies.get("rotors")
        rotors = json.loads(rotors)
        rotor = rotors[rotornr]
        response = app.make_response(jsonify("Rotor position of rotor " + str(rotor) + " set to " + str(position)))
        set_cookie(response, "positions", json.dumps(positions))
        return response


# Endpoint to get the available reflector of a specific variant
@app.route('/reflectors', methods=['GET'])
def get_reflectors():
    variant_cookie = request.cookies.get('variant')
    if not variant_cookie:
        return 'Variant cookie not set', 400

    with open("/etc/enigma.yaml", "r") as file:
        data = yaml.load(file, Loader=yaml.SafeLoader)

    variant = data['variants'].get(variant_cookie)
    if not variant:
        return 'Variant not found in YAML', 400

    reflectors = []
    reflector_info = variant['reflectors']
    available_reflectors = reflector_info.keys()
    for reflector_name, reflector_data in reflector_info.items():
        reflector = {
            'name': reflector_name,
            'wiring': reflector_data
        }
        reflectors.append(reflector)

    return jsonify(reflectors)


# Endpoint to set and get the current reflector
@app.route('/reflector', methods=['GET', 'PUT'])
def set_reflector():
    variant_cookie = request.cookies.get('variant')
    if not variant_cookie:
        return jsonify('Variant cookie not set', 400)

    reflector_cookie = request.cookies.get('reflector')

    if request.method == 'GET':
        reflector = reflector_cookie
        response_data = {'reflector': reflector} if reflector is not None else ('Variant cookie not set', 400)
        return jsonify(response_data)
    elif request.method == 'PUT':
        reflector = request.get_json()['reflector']

        with open("/etc/enigma.yaml", "r") as file:
            data = yaml.load(file, Loader=yaml.SafeLoader)

        variant = data['variants'].get(variant_cookie)
        if not variant:
            return 'Variant not found in YAML', 400

        valid_reflectors = variant['reflectors'].keys()
        if reflector not in valid_reflectors:
            return 'Invalid reflector for the selected variant', 400

        response = app.make_response(jsonify("Reflector " + str(reflector) + " set"))
        set_cookie(response, "reflector", reflector)
        return response


# Endpoint to retrieve the input history and regular history
@app.route("/history", methods=['GET'])
def get_history():
    input_history = request.cookies.get("input_history") or ""
    history = request.cookies.get("history") or ""
    return jsonify({"input_history": input_history, "history": history})


# Endpoint for setting and retrieving the plugboard
@app.route("/plugboard", methods=["GET", "PUT"])
def handle_plugboard():
    if request.method == "GET":
        plugboard_cookie = request.cookies.get("plugboard")
        if plugboard_cookie:
            plugboard_dict = ast.literal_eval(plugboard_cookie)
            return jsonify(plugboard_dict)
        else:
            return "Plugboard cookie not set", 400
    elif request.method == "PUT":
        plugboard = request.get_json()["plugboard"]
        response = app.make_response(jsonify("Plugboard updated"))
        set_cookie(response, "plugboard", plugboard)
        return response


# Endpoint for resetting the Enigma
@app.route('/reset', methods=["GET"])
def reset_enigma():
    response = jsonify("Enigma reset")
    cookies = ["variant", "plugboard", "rotors", "positions", "input_history", "history", "reflector"]
    for cookie in cookies:
        response.set_cookie(cookie, "", expires=0)
    return response


single_request = Lock()


# Endpoint for encrypting a letter
@app.route('/encrypt', methods=['PUT'])
def encrypt_letter():

    ukw_b = 'YRUHQSLDPXNGOKMIEBFZCWVJAT'

    if single_request.locked():
        return str(), 423

    with single_request:
        # Reading the cookie values
        variant = request.cookies.get("variant") or 'I'
        positions = request.cookies.get("positions") or '["A", "A", "A"]'
        rotors = request.cookies.get("rotors") or '["I","II","III"]'
        plugboard = request.cookies.get("plugboard") or "{}"
        ukw = request.cookies.get("reflector") or 'UKW-B'

        positions = json.loads(positions)
        rotors = json.loads(rotors)

        rotor_mapping = []
        notches = []

        with open("/etc/enigma.yaml", "r") as stream:
            data = yaml.safe_load(stream)

        rotor_config = data['variants'][variant]['rotors']
        ukw = data['variants'][variant]['reflectors'][ukw]
        for rotor in rotors:
            notches.append(rotor_config[rotor]['turnover'])
            rotor_mapping.append((rotor_config[rotor]['substitution']))


        enigma = Enigma(rotor1=rotor_mapping[0], rotor2=rotor_mapping[1], rotor3=rotor_mapping[2],
                        start_pos1=positions[0], start_pos2=positions[1], start_pos3=positions[2],
                        reflector=ukw,
                        notch_rotor1=notches[0], notch_rotor2=notches[1], notch_rotor3=notches[2])

        # Set the plugboard (Will be saved as dictionary) -> Important step to use apply_plugboard
        enigma.set_plugboard(plugboard)

        # Encryption process: Getting the letter -> Encrypting -> Saving the new positions
        data = request.get_json()
        letter = data.get('letter')
        input_letter = letter
        letter = enigma.encrypt_letter(letter)
        positions = enigma.get_rotor_positions()
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
