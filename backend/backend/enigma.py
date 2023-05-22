from backend.backend.rotor import Rotor, index_from_letter, letter_from_index


class Enigma:
    def __init__(self, rotor1, rotor2, rotor3, start_pos1, start_pos2, start_pos3, reflector, notch_rotor1,
                 notch_rotor2, notch_rotor3, plugboard=None):

        self.first_rotor = Rotor(rotor1, start_pos1, notch_rotor1)
        self.second_rotor = Rotor(rotor2, start_pos2, notch_rotor2)
        self.third_rotor = Rotor(rotor3, start_pos3, notch_rotor3)

        self.rotor_list = [self.first_rotor, self.second_rotor, self.third_rotor]

        self.reflector = reflector
        self.plugboard = plugboard or {}

    def set_rotor_positions(self, pos1, pos2, pos3):
        self.first_rotor.set_position(pos1)
        self.second_rotor.set_position(pos2)
        self.third_rotor.set_position(pos3)

    def set_plugboard(self, plugboard):
        self.plugboard = plugboard

    def step_rotors(self):
        """
        Rotates the rotors by one position.
        """
        # Rotors are = |Third|Second|First|. The first one always steps.

        # Checking if we need to rotate the second and third rotor based on notches and current postions
        if self.first_rotor.position == self.first_rotor.notch:
            if self.second_rotor.position == self.second_rotor.notch:

                self.third_rotor.step_rotor()
            self.second_rotor.step_rotor()
        self.first_rotor.step_rotor()

    def apply_plugboard(self, letter):
        return self.plugboard.get(letter, letter)

    def encrypt_forward(self, letter):
        """
        Encrypts a letter in the forward direction |reflector <- Third rotor <- Second rotor  <- First rotor <- input
        :param letter: Any capital letter
        :return:  The capital letter after encryption by three rotors, before reflection!
        """
        relative_offset = 0  # The relative offset between two rotors. Starts at 0 since the first rotor has none

        for rotor in self.rotor_list:
            letter_index = index_from_letter(letter)    # gets a number that represents our letter to do math
            relative_offset = rotor.offset - relative_offset    # removes the offset of the previous rotor
            letter_index = (letter_index + relative_offset) % 26  # adds the offset to the letter
            letter = letter_from_index(letter_index)

            letter = rotor.encrypt_character(letter)  # encrypts the letter using the current rotor

            relative_offset = rotor.offset  # saves the current rotors offset for the next rotor relative offset

        return letter

    def encrypt_backward(self, letter):
        # Get relative offsets for both rotors
        relative_offset = 0
        for rotor in reversed(self.rotor_list):  # Reverse the rotor list
            letter_index = index_from_letter(letter)  # gets a number that represents our letter to do math

            relative_offset = rotor.offset - relative_offset  # removes the offset of the previous rotor

            letter_index = (letter_index + relative_offset) % 26  # adds the offset to the letter

            letter = letter_from_index(letter_index)
            letter = rotor.encrypt_character_reverse(letter)  # encrypts the letter using the current rotor

            relative_offset = rotor.offset  # saves the current rotors offset for the next rotor relative offset

        # remove the first rotors offset from letter. Since we don't have an entry rotor (ETW)
        letter_index = index_from_letter(letter)
        letter_index = (letter_index - self.first_rotor.offset) % 26
        letter = letter_from_index(letter_index)
        return letter

    def reflect(self, letter):
        letter_index = index_from_letter(letter)
        offset = self.third_rotor.offset

        reflect_position = letter_index - offset

        return self.reflector[reflect_position]

    def encrypt_letter(self, letter):
        self.step_rotors()

        letter = self.encrypt_forward(letter)

        letter = self.reflect(letter)

        letter = self.encrypt_backward(letter)

        return letter


def next_letter(letter):
    """
    Returns the next letter in the alphabet looping at Z
    """
    if letter == 'Z':
        next_letter_result = 'A'
    else:
        next_letter_result = chr(ord(letter) + 1)

    return next_letter_result
