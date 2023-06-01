from flask import Flask, jsonify, request, json
from flask import current_app as app
from threading import Lock
from .enigma import Enigma
import yaml


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
            return "Variant cookie not set", 400
    elif request.method == "PUT":
        variant = request.get_json()["variant"]
        response = app.make_response(jsonify("Variant " + variant + " set!"))
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
        if rotor not in valid_rotors:
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
    # Cookie / Anfrage verarbeitung

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
        # Reading the cookie values
        variant = request.cookies.get("variant") or 'I'
        positions = request.cookies.get("positions") or '["A", "A", "A"]'
        rotors = request.cookies.get("rotors") or '["I","II","III"]'

        positions = json.loads(positions)
        rotors = json.loads(rotors)

        rotor_mapping = []
        notches = []

        with open("/etc/enigma.yaml", "r") as stream:
            try:
                rotor_config = yaml.safe_load(stream)['variants'][variant]['rotors']
                for rotor in rotors:
                    notches.append(rotor_config[rotor]['turnover'])
                    rotor_mapping.append((rotor_config[rotor]['substitution']))
            except yaml.YAMLError as exc:
                print(exc)

        # TODO: Notch für rotor laden aus YAML für entsprechende Variante

        # notches = fetch_notches(variant, rotors)
        # notch_rotor1 = notches[1] ....

        enigma = Enigma(rotor1=rotor_mapping[0], rotor2=rotor_mapping[1], rotor3=rotor_mapping[2],
                        start_pos1=positions[0], start_pos2=positions[1], start_pos3=positions[2],
                        reflector=ukw_b,
                        notch_rotor1=notches[0], notch_rotor2=notches[1], notch_rotor3=notches[2])

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
