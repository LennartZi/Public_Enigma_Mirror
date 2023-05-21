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

    def encode_forward(self, letter, rotor_offset):
        temp_offset = None

        for i in range(2, -1, -1):

            if i == 1 and rotor_offset[2] != 0:
                temp_offset = rotor_offset[i]
                rotor_offset[i] = rotor_offset[i] - rotor_offset[i + 1]

            elif i == 0 and rotor_offset[1] != 0:
                temp_offset = rotor_offset[i]
                rotor_offset[i] = rotor_offset[i] - rotor_offset[i + 1]

            letter_idx = ord(letter) - ord('A')
            letter_idx = (letter_idx + rotor_offset[i]) % 26

            letter = chr(ord(self.rotor_list[i][letter_idx]))

            if temp_offset is not None:
                rotor_offset[i] = temp_offset
                temp_offset = None

        letter_index = ord(letter) - ord('A')
        letter_index_adjusted = (letter_index - rotor_offset[0]) % 26
        encoded_letter = chr(letter_index_adjusted + ord('A'))

        return encoded_letter

    def encrypt_forward(self, letter):
        # get relative offsets for both rotors
        relative_offset = 0

        for rotor in self.rotor_list:
            letter_index = index_from_letter(letter)    # gets a number that represents our letter to do math

            relative_offset = rotor.offset - relative_offset

            letter_index = (letter_index + relative_offset) % 26  # adds the offset to the letter
            # print(f"letter_index: {letter_index}")

            letter = letter_from_index(letter_index)

            letter = rotor.encrypt_character(letter)

            relative_offset = rotor.offset


        # add rotor offset to the letter

        #
        return letter

    def encrypt_backward(self, letter):
        pass

    def encode_reverse(self, letter, rotor_offset):
        temp_offset = None

        for i in range(3):

            if i == 1 and rotor_offset[0] != 0:
                temp_offset = rotor_offset[i]
                rotor_offset[i] = rotor_offset[i] - rotor_offset[i - 1]

            elif i == 2 and rotor_offset[1] != 0:
                temp_offset = rotor_offset[i]
                rotor_offset[i] = rotor_offset[i] - rotor_offset[i - 1]

            letter_idx = self.rotor_list[i].index(chr(((ord(letter) - ord('A') + rotor_offset[i]) % 26) + ord('A')))
            letter = chr(letter_idx + ord('A'))

            if temp_offset is not None:
                rotor_offset[i] = temp_offset
                temp_offset = None

        letter = chr(((ord(letter) - ord('A') - rotor_offset[2]) % 26) + ord('A'))
        return letter

    def reflect(self, letter, rotor_offset):
        letter_idx = ord(letter) - ord('A') - rotor_offset

        return self.reflector[letter_idx]

    def encode_letter(self, letter):
        # Step rotors
        self.step_rotors()

        # Apply plugboard
        letter = self.apply_plugboard(letter)

        # ###rotor_offset = self.calculate_rotor_offset()

        # Encode through rotors in forward direction (I -> II -> III -> Reflector)
        # ###letter = self.encode_forward(letter, rotor_offset)

        # Reflect through reflector
        # ###letter = self.reflect(letter, rotor_offset[0])

        # Encode through rotors in reverse direction (Reflector -> III -> II -> I)
        # ###letter = self.encode_reverse(letter, rotor_offset)

        # Apply plugboard
        letter = self.apply_plugboard(letter)

        return letter

    def encrypt_letter(self, letter):
        self.step_rotors()

        letter = self.encrypt_forward()

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
