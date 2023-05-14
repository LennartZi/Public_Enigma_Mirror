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

        notch_rotor1='B', notch_rotor2='X', notch_rotor3='F')

    enigma_machine.set_plugboard({'A': 'Z', 'B': 'Y', 'C': 'X', 'D': 'W', 'E': 'V', 'F': 'U', 'G': 'T', 'H': 'S',
                                  'I': 'R', 'J': 'Q', 'K': 'P', 'L': 'O', 'M': 'N'})
    enigma_machine.set_rotor_positions('A', 'B', 'C')

    yield enigma_machine

    # teardown code
    enigma_machine.set_rotor_positions('A', 'B', 'C')
    enigma_machine.set_plugboard({'A': 'Z', 'B': 'Y', 'C': 'X', 'D': 'W', 'E': 'V', 'F': 'U', 'G': 'T', 'H': 'S',
                                  'I': 'R', 'J': 'Q', 'K': 'P', 'L': 'O', 'M': 'N'})


def test_step_one_rotor(enigma_machine):
    # Test one rotor stepping
    enigma_machine.set_rotor_positions('A', 'B', 'C')
    enigma_machine.step_rotors()
    assert enigma_machine.rotor_positions == ['A', 'B', 'D']

    # second step
    enigma_machine.step_rotors()
    assert enigma_machine.rotor_positions == ['A', 'B', 'E']

    # stepping through the whole range up to 'B', the notch position
    for i in range(23):
        enigma_machine.step_rotors()
    assert enigma_machine.rotor_positions == ['A', 'B', 'B']


def test_step_two_rotors(enigma_machine):
    # Test two rotors stepping
    enigma_machine.set_rotor_positions('A', 'B', 'B')
    enigma_machine.step_rotors()
    assert enigma_machine.rotor_positions == ['A', 'C', 'C']


def test_step_three_rotors(enigma_machine):
    # Test three rotors stepping
    enigma_machine.set_rotor_positions('A', 'B', 'B')
    enigma_machine.step_rotors()
    assert enigma_machine.rotor_positions == ['A', 'C', 'C']
