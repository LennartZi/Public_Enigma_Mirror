from backend.backend.enigma import Enigma
import pytest


@pytest.fixture()
def enigma_machine():
    enigma_machine = Enigma(
        rotor1=['E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O', 'W', 'Y', 'H', 'X', 'U', 'S', 'P', 'A',
                'I', 'B', 'R', 'C', 'J'],

        rotor2=['A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W', 'T', 'M', 'C', 'Q', 'G', 'Z', 'N', 'P',
                'Y', 'F', 'V', 'O', 'E'],

        rotor3=['B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V', 'Z', 'N', 'Y', 'E', 'I', 'W', 'G', 'A', 'K',
                'M', 'U', 'S', 'Q', 'O'],

        start_pos1='B', start_pos2='D', start_pos3='F',

        reflector=['Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O', 'K', 'M', 'I', 'E', 'B', 'F', 'Z',
                   'C', 'W', 'V', 'J', 'A', 'T'],

        notch_rotor1='Q', notch_rotor2='E', notch_rotor3='V')

    enigma_machine.set_rotor_positions('A', 'A', 'A')

    yield enigma_machine

    # teardown code
    enigma_machine.set_rotor_positions('A', 'B', 'C')


def test_step_one_rotor(enigma_machine):
    # Test one rotor stepping
    enigma_machine.set_rotor_positions('A', 'B', 'R')
    enigma_machine.step_rotors()
    assert enigma_machine.rotor_positions == ['A', 'B', 'S']

    # second step
    enigma_machine.step_rotors()
    assert enigma_machine.rotor_positions == ['A', 'B', 'T']

    # stepping through the whole range up to 'B', the notch position
    for i in range(23):
        enigma_machine.step_rotors()
    assert enigma_machine.rotor_positions == ['A', 'B', 'Q']


def test_step_two_rotors(enigma_machine):
    # Test two rotors stepping
    enigma_machine.set_rotor_positions('A', 'B', 'Q')
    enigma_machine.step_rotors()
    assert enigma_machine.rotor_positions == ['A', 'C', 'R']


def test_step_three_rotors(enigma_machine):
    # Test three rotors stepping
    enigma_machine.set_rotor_positions('A', 'E', 'Q')
    enigma_machine.step_rotors()
    assert enigma_machine.rotor_positions == ['B', 'F', 'R']


def test_encrypt_sentence(enigma_machine):
    # Tests the encryption of a sentence
    enigma_machine.set_rotor_positions('A', 'A', 'A')

    # Sentence currently without spaces and all uppercase!
    sentence = "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS"
    encrypted_word = ""

    # Sentence is split into letters and encrypted one by one
    for letter in sentence:
        encrypted_letter = enigma_machine.encode_letter(letter)
        encrypted_word += encrypted_letter

    # expected result from https://people.physik.hu-berlin.de/~palloks/js/enigma/enigma-u_v20.html
    assert encrypted_word == "ZPJJSVSPGBWNXCQXOPCCFYXRPWVYUAXQRZBKKMJZNOFHLCCPGICCVZZ"


def test_decrypt_sentence(enigma_machine):
    # Tests the decryption of a sentence
    enigma_machine.set_rotor_positions('A', 'A', 'A')

    # Sentence currently without spaces and all uppercase!
    sentence = "ZPJJSVSPGBWNXCQXOPCCFYXRPWVYUAXQRZBKKMJZNOFHLCCPGICCVZZ"
    decrypted_word = ""

    # Sentence is split into letters and encrypted one by one
    for letter in sentence:
        encrypted_letter = enigma_machine.encode_letter(letter)
        decrypted_word += encrypted_letter

    assert decrypted_word == "THISISATESTOFTHEENIGMAENCRYPTIONANDDECRYPTIONALGORITHMS"


