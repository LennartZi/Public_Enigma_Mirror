from .rotor import Rotor, index_from_letter, letter_from_index


class Enigma:
    def __init__(self, rotor1, rotor2, start_pos1, start_pos2, reflector, notch_rotor1, notch_rotor2,
                 plugboard=None, rotor3=None, start_pos3=None,  notch_rotor3=None):

        self.first_rotor = Rotor(rotor1, start_pos1, notch_rotor1)
        self.second_rotor = Rotor(rotor2, start_pos2, notch_rotor2)

        # Used to iterate through all rotors later on. We can use this to deal with the 2 rotor variant
        self.rotor_list = [self.first_rotor, self.second_rotor]

        # If we are handed a third rotor for construction use it and add the third rotor to the list
        if rotor3 is not None:
            self.third_rotor = Rotor(rotor3, start_pos3, notch_rotor3)
            self.rotor_list.append(self.third_rotor)

        self.reflector = reflector
        self.plugboard = plugboard or {}

    def set_plugboard(self, plugboard):
        """
        currently not implemented or tested
        :param plugboard:
        :return:
        """
        self.plugboard = plugboard

    def apply_plugboard(self, letter):
        """
        currently not implemented or tested
        :param letter:
        :return:
        """
        return self.plugboard.get(letter, letter)

    def set_rotor_positions(self, pos1, pos2, pos3=None):
        """
        Sets all rotors to any chosen position
        This is a legacy function that lets us not change any of the frontend stuff.
        :param pos1: position for rotor 1 given as a capital letter
        :param pos2: position for rotor 2 given as a capital letter
        :param pos3: position for rotor 3 given as a capital letter
        """
        positions = [pos1, pos2, pos3]  # this is hacky and should probably be changed
        i = 0
        for rotor in self.rotor_list:
            rotor.position = positions[i]
            i += 1
        # TODO: Add handling for when pos3 is not supplied but we have 3 rotors

    def step_rotors(self):
        """
        Rotates the rotors by one position.
        """
        # Rotors are = |Third|Second|First|. The first one always steps.
        for rotor in self.rotor_list:
            position = rotor.position  # this saves the position of the rotor before stepping

            rotor.step_rotor()

            if position != rotor.notch:  # If we weren't on the notch we don't move the next rotor
                break

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

            relative_offset = rotor.offset  # saves the current rotors offset for the next rotors relative offset

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
        offset = self.rotor_list[-1].offset  # this is always the last rotor

        reflect_position = letter_index - offset

        return self.reflector[reflect_position]

    def encrypt_letter(self, letter):
        """
        Encrypts a letter and returns the encrypted one
        :param letter: Letter that needs to be de/encrypted
        :return: The encrypted letter
        """
        self.step_rotors()

        # Plugboard goes here

        # reflector <- Third rotor <- Second rotor  <- First rotor <- input
        letter = self.encrypt_forward(letter)

        letter = self.reflect(letter)

        # reflector -> Third rotor -> Second rotor  -> First rotor -> output
        letter = self.encrypt_backward(letter)

        # Plugboard goes here

        return letter

    def get_rotor_positions(self):
        """
        Returns position of all rotors as a list
        :return: [first rotor, second rotor, third rotor]
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
