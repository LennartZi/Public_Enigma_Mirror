from backend.enigma import Enigma, next_letter
import pytest


@pytest.fixture()
def enigma_machine():
    """
    Enigma M3 with rotors: I, II, III reflector: UKW-B and no Plugboard
    """
    enigma_machine = Enigma(
        rotor1=['E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O', 'W', 'Y', 'H', 'X', 'U', 'S', 'P', 'A',
                'I', 'B', 'R', 'C', 'J'],

        rotor2=['A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W', 'T', 'M', 'C', 'Q', 'G', 'Z', 'N', 'P',
                'Y', 'F', 'V', 'O', 'E'],

        rotor3=['B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V', 'Z', 'N', 'Y', 'E', 'I', 'W', 'G', 'A', 'K',
                'M', 'U', 'S', 'Q', 'O'],

        start_pos1='A', start_pos2='A', start_pos3='A',

        reflector=['Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O', 'K', 'M', 'I', 'E', 'B', 'F', 'Z',
                   'C', 'W', 'V', 'J', 'A', 'T'],

        notch_rotor1='Q', notch_rotor2='E', notch_rotor3='V',
        plugboard=None)

    enigma_machine.set_rotor_positions('A', 'A', 'A')

    yield enigma_machine

    # teardown code
    plugboard = None
    enigma_machine.set_rotor_positions('A', 'A', 'A')


@pytest.fixture()
def two_rotor_enigma():
    """
    Two rotor enigma, currently just an M3 with rotors I, II reflector UKW-B, and no Plugboard
    """
    # TODO: Change rotors and notches to fit, write more test than just the one
    two_rotor_enigma = Enigma(
        rotor1=['E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O', 'W', 'Y', 'H', 'X', 'U', 'S', 'P',
                'A',
                'I', 'B', 'R', 'C', 'J'],

        rotor2=['A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W', 'T', 'M', 'C', 'Q', 'G', 'Z', 'N',
                'P',
                'Y', 'F', 'V', 'O', 'E'],

        start_pos1='A', start_pos2='A',

        reflector=['Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O', 'K', 'M', 'I', 'E', 'B', 'F',
                   'Z',
                   'C', 'W', 'V', 'J', 'A', 'T'],

        notch_rotor1='Q', notch_rotor2='E')

    two_rotor_enigma.set_rotor_positions('A', 'A')

    yield two_rotor_enigma

    # teardown code
    two_rotor_enigma.set_rotor_positions('A', 'A')


def test_get_rotor_positions(enigma_machine):
    enigma_machine.set_rotor_positions('X', 'V', 'B')
    positions = enigma_machine.get_rotor_positions()
    assert positions == ['X', 'V', 'B']
    # These two tests seem a bit stupid since they do the same thing


def test_set_rotor_position(enigma_machine):
    enigma_machine.set_rotor_positions('X', 'V', 'B')
    positions = enigma_machine.get_rotor_positions()
    assert positions == ['X', 'V', 'B']
    # These two tests seem a bit stupid since they do the same thing


def test_next_letter():
    assert next_letter('F') == 'G'
    assert next_letter('Z') == 'A'


def test_apply_plugboard(enigma_machine):
    enigma_machine.plugboard = {'A': 'B', 'B': 'A'}

    result1 = enigma_machine.apply_plugboard("A")
    result2 = enigma_machine.apply_plugboard("B")

    assert result1 == "B"
    assert result2 == "A"


def test_set_plugboard(enigma_machine):
    plugboard = "{'A': 'B', 'C': 'D', 'F': 'L', 'X': 'M'}"
    enigma_machine.set_plugboard(plugboard)

    assert enigma_machine.plugboard == {'A': 'B', 'B': 'A',
                                        'C': 'D', 'D': 'C',
                                        'F': 'L', 'L': 'F',
                                        'X': 'M', 'M': 'X'}

def test_step_one_rotor(enigma_machine):
    # Test one rotor stepping
    enigma_machine.set_rotor_positions('R', 'A', 'A')
    enigma_machine.step_rotors()
    assert (
        enigma_machine.first_rotor.position,
        enigma_machine.second_rotor.position,
        enigma_machine.third_rotor.position,
    ) == ('S', 'A', 'A'), "Rotor positions after stepping are incorrect."

    # second step
    enigma_machine.step_rotors()
    assert (
        enigma_machine.first_rotor.position,
        enigma_machine.second_rotor.position,
        enigma_machine.third_rotor.position,
    ) == ('T', 'A', 'A'), "Rotor positions after stepping are incorrect."

    # stepping through the whole range up to 'Q', the notch position
    for i in range(23):
        enigma_machine.step_rotors()
    assert (
        enigma_machine.first_rotor.position,
        enigma_machine.second_rotor.position,
        enigma_machine.third_rotor.position,
    ) == ('Q', 'A', 'A'), "Rotor positions after stepping 23times are incorrect."


def test_step_two_rotors(enigma_machine):
    # Test two rotors stepping
    enigma_machine.set_rotor_positions('Q', 'A', 'A')
    enigma_machine.step_rotors()
    assert (
        enigma_machine.first_rotor.position,
        enigma_machine.second_rotor.position,
        enigma_machine.third_rotor.position,
    ) == ('R', 'B', 'A'), "Rotor positions after stepping two rotors are incorrect."


def test_step_three_rotors(enigma_machine):
    # Test three rotors stepping
    enigma_machine.set_rotor_positions('Q', 'E', 'A')
    enigma_machine.step_rotors()
    assert (
        enigma_machine.first_rotor.position,
        enigma_machine.second_rotor.position,
        enigma_machine.third_rotor.position,
    ) == ('R', 'F', 'B'), "Rotor positions after stepping three rotors are incorrect."


def test_encrypt_letter_forward(enigma_machine):
    enigma_machine.set_rotor_positions('Q', 'E', 'A')
    enigma_machine.step_rotors()  # Stepping the rotor. The function would usually only be called after a step

    result = enigma_machine.encrypt_forward('T')

    assert result == 'L'


def test_reflector(enigma_machine):
    enigma_machine.set_rotor_positions('Q', 'E', 'A')

    result = enigma_machine.reflect('K')

    assert result == 'N'


def test_encrypt_letter_backward(enigma_machine):
    enigma_machine.set_rotor_positions('Q', 'E', 'A')
    enigma_machine.step_rotors()    # Stepping the rotor. The function would usually only be called after a step

    result = enigma_machine.encrypt_backward('N')

    assert result == 'V'


def test_encrypt_sentence(enigma_machine):
    # Tests the encryption of a sentence
    enigma_machine.set_rotor_positions('Q', 'E', 'A')

    # Sentence currently without spaces and all uppercase!
    sentence = "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS" \
               "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS" \
               "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS" \
               "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS" \
               "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS" \
               "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS"
    encrypted_sentence = ""

    # Sentence is split into letters and encrypted one by one
    for letter in sentence:
        encrypted_letter = enigma_machine.encrypt_letter(letter)
        encrypted_sentence += encrypted_letter

    # expected result from https://people.physik.hu-berlin.de/~palloks/js/enigma/enigma-u_v20.html
    assert encrypted_sentence == "VXCJNEYKDLWBKXSLAKXXDFJQSEGCATFIQTBKLDKURCJVVZTISTABSAJ" \
                                 "SQNUOGJCCIOTLQUHGOXCXPUIGLVYOJSVUPWMPIKJEDHDJYUHAIFFXFJ" \
                                 "NIOAPMHHXUHREBSICOUKLULXNWGJOMFKWLQAVJHIKSJRGEVNTLEESFO" \
                                 "PLZDOVQRBNFEEAICKKYTIWIVXJUIALSVLPWZFBTDEUSQHPGWFGQOGOX" \
                                 "YCGPVTTXZKUUKFNWDIDRPIWSEBHKPSBGQHBNDDSWEBKDJNZXVVCXEBI" \
                                 "YEHWQARXONGNUVIAOWNRKOYPQVQGRZKAYVCNRQDWXBQKWONKYHSOEEO"


def test_decrypt_sentence(enigma_machine):
    # Tests the decryption of a sentence
    enigma_machine.set_rotor_positions('Q', 'E', 'A')

    # Sentence currently without spaces and all uppercase!
    sentence = "VXCJNEYKDLWBKXSLAKXXDFJQSEGCATFIQTBKLDKURCJVVZTISTABSAJ" \
               "SQNUOGJCCIOTLQUHGOXCXPUIGLVYOJSVUPWMPIKJEDHDJYUHAIFFXFJ" \
               "NIOAPMHHXUHREBSICOUKLULXNWGJOMFKWLQAVJHIKSJRGEVNTLEESFO" \
               "PLZDOVQRBNFEEAICKKYTIWIVXJUIALSVLPWZFBTDEUSQHPGWFGQOGOX" \
               "YCGPVTTXZKUUKFNWDIDRPIWSEBHKPSBGQHBNDDSWEBKDJNZXVVCXEBI" \
               "YEHWQARXONGNUVIAOWNRKOYPQVQGRZKAYVCNRQDWXBQKWONKYHSOEEO"
    decrypted_sentence = ""

    # Sentence is split into letters and encrypted one by one
    for letter in sentence:
        encrypted_letter = enigma_machine.encrypt_letter(letter)
        decrypted_sentence += encrypted_letter

    assert decrypted_sentence == "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS" \
                                 "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS" \
                                 "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS" \
                                 "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS" \
                                 "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS" \
                                 "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS"


def test_get_rotor_position(enigma_machine):
    enigma_machine.set_rotor_positions('A', 'B', 'C')

    assert enigma_machine.get_rotor_positions() == ['A', 'B', 'C']


def test_two_rotor_step(two_rotor_enigma):
    # Test stepping both rotors
    two_rotor_enigma.set_rotor_positions('Q', 'A')
    two_rotor_enigma.step_rotors()
    assert (
               two_rotor_enigma.first_rotor.position,
               two_rotor_enigma.second_rotor.position
           ) == ('R', 'B'), "Rotor positions after stepping two rotors are incorrect."
