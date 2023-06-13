from backend.rotor import Rotor, index_from_letter, letter_from_index
import pytest


# Testing of the two non-class functions
def test_index_from_letter():
    # "A" should be 0 and "Z" should be 25
    index = index_from_letter('Z')

    assert index == 25


def test_letter_from_index():
    # 0 should be "A" and 25 should be "Z"
    letter = letter_from_index(25)

    assert letter == 'Z'


@pytest.fixture()
def rotor_1():
    """
    Rotor I of the M3 enigma variant
    """
    rotor_1 = Rotor(
        rotor_mapping=['E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O', 'W', 'Y', 'H', 'X', 'U', 'S',
                       'P', 'A', 'I', 'B', 'R', 'C', 'J'],
        position='A',
        notch='Q'
    )

    yield rotor_1

    # teardown
    position = 'A'


def test_calculate_offset(rotor_1):
    # Tests if the calculate_offset function correctly applies the offset to the class
    rotor_1.position ='C'
    rotor_1.calculate_offset()

    # distance from 'C' to 'A' is 2, check function comments for details
    assert rotor_1.offset == 2


def test_set_position(rotor_1):
    # Tests the rotor set_position function
    rotor_1.set_position('Z')

    assert rotor_1.position == 'Z'


def test_step_rotor_position_a(rotor_1):
    # Tests stepping in a normal scenario
    rotor_1.set_position('A')
    rotor_1.step_rotor()

    assert rotor_1.position == 'B'


def test_step_rotor_set_position_z(rotor_1):
    # Tests stepping in the edge case of being stepping from "Z" to "A"
    rotor_1.set_position('Z')
    rotor_1.step_rotor()

    assert rotor_1.position == 'A'


def test_encrypt_character(rotor_1):
    """
    Tests the encryption of a letter through the first rotor. This ends up being pretty hacky because a large part
    of this process is handled in the Enigma class, not the rotor class.
    This test is very volatile and should be treated with caution :)
    """
    rotor_1.set_position('A')
    rotor_1.step_rotor()
    letter = 'G'

    # this block of code is found in the enigma when it the ROTOR function class.
    letter_index = index_from_letter(letter)    # gets a number that represents our letter to do math
    letter_index = letter_index + rotor_1.offset  # adds rotor offset to letter, CAREFUL!! when this gets > 26 it breaks
    letter = letter_from_index(letter_index)

    encrypted_char = rotor_1.encrypt_character(letter)  # actual function we want to test

    assert encrypted_char == 'Q'


def test_encrypt_backward(rotor_1):
    """
    Tests the encryption of a letter through the first rotor. This ends up being pretty hacky because a large part
    of this process is handled in the Enigma class, not the rotor class.
    This test is very volatile and should be treated with caution :)
    """
    rotor_1.set_position('A')
    rotor_1.step_rotor()
    letter = 'I'

    # this block of code is found in the enigma class.
    letter_index = index_from_letter(letter)  # gets a number that represents our letter to do math
    letter_index = letter_index + rotor_1.offset  # adds rotor offset to letter, CAREFUL!! when this gets > 26 it breaks
    letter = letter_from_index(letter_index)

    encrypted_char = rotor_1.encrypt_character_reverse(letter)  # actual function we want to test

    assert encrypted_char == "Z"

