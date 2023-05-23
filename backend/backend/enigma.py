from backend.backend.rotor import Rotor, index_from_letter, letter_from_index


class Enigma:
    def __init__(self, rotor1, rotor2, rotor3, start_pos1, start_pos2, start_pos3, reflector, notch_rotor1,
                 notch_rotor2, notch_rotor3, plugboard=None):

        self.first_rotor = Rotor(rotor1, start_pos1, notch_rotor1)
        self.second_rotor = Rotor(rotor2, start_pos2, notch_rotor2)
        self.third_rotor = Rotor(rotor3, start_pos3, notch_rotor3)

        # Used to iterate through all rotors later on. We can use this to deal with the 2 rotor variant
        self.rotor_list = [self.first_rotor, self.second_rotor, self.third_rotor]

        self.reflector = reflector
        self.plugboard = plugboard or {}

    def set_rotor_positions(self, pos1, pos2, pos3):
        """
        Sets all rotors to any chosen position
        This is a legacy function that lets us not change any of the frontend stuff.
        :param pos1: position for rotor 1 given as a capital letter
        :param pos2: position for rotor 2 given as a capital letter
        :param pos3: position for rotor 3 given as a capital letter
        """
        self.first_rotor.set_position(pos1)
        self.second_rotor.set_position(pos2)
        self.third_rotor.set_position(pos3)

    def set_plugboard(self, plugboard):
        # TODO: add functionality and test
        """
        currently not implemented or tested
        :param plugboard:
        :return:
        """
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
        self.get_rotor_positions()

    def apply_plugboard(self, letter):
        # TODO: add functionality and test
        """
        currently not implemented or tested
        :param letter:
        :return:
        """
        return self.plugboard.get(letter, letter)

    def encrypt_forward(self, letter):
        """
        Encrypts a letter in the forward direction |reflector <- Third rotor <- Second rotor  <- First rotor <- input
        :param letter: Any capital letter
        :return:  The capital letter after encryption by three rotors, ***before*** reflection!
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
        """
        Encrypts a letter in the backward direction |reflector -> Third rotor -> Second rotor  -> First rotor -> output
        :param letter: Any capital letter
        :return:  The capital letter after encryption by three rotors, ***after*** reflection!
        """
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
        """
        Reflects the letter using the reflector
        :param letter: Capital letter to reflect
        :return: Capital letter after reflection
        """
        letter_index = index_from_letter(letter)
        offset = self.third_rotor.offset

        reflect_position = letter_index - offset

        return self.reflector[reflect_position]

    def encrypt_letter(self, letter):
        """
        Encrypts a letter and returns the encrypted one
        :param letter: Letter that needs to be de/encrypted
        :return: The encrypted letter
        """
        self.step_rotors()

        # TODO: add plugboard here
        # reflector <- Third rotor <- Second rotor  <- First rotor <- input
        letter = self.encrypt_forward(letter)

        letter = self.reflect(letter)

        # reflector -> Third rotor -> Second rotor  -> First rotor -> output
        letter = self.encrypt_backward(letter)

        # TODO: add plugboard here
        return letter

    def encode_letter(self, letter):
        # TODO: remove and change calls in api to encrypt_letter
        """
        Encrypts any given letter
        Only used to call encrypt_letter. This is a legacy function and should be removed
        :param letter: letter we want to encrypt
        :return: encrypted letter
        """

        return self.encrypt_letter(letter)

    def get_rotor_positions(self):
        """
        Returns position of all rotors as a list
        :return: [first_rotor, second_rotor, third_rotor]
        """
        rotor_positions = []
        for rotor in self.rotor_list:  # reverse list if you'd like them returned as [3,2,1]
            rotor_positions.append(rotor.position)

        return rotor_positions


def next_letter(letter):
    """
    Returns the next letter in the alphabet looping at Z
    """
    if letter == 'Z':
        next_letter_result = 'A'
    else:
        next_letter_result = chr(ord(letter) + 1)

    return next_letter_result
