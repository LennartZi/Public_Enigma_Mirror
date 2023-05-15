class Enigma:
    def __init__(self, rotor1, rotor2, rotor3, start_pos1, start_pos2, start_pos3, reflector, notch_rotor1,
                 notch_rotor2, notch_rotor3, plugboard=None):
        self.rotors = [rotor3, rotor2, rotor1]
        self.rotor_positions = [start_pos3, start_pos2, start_pos1]
        self.reflector = reflector
        self.plugboard = plugboard or {}
        self.notches = [notch_rotor3, notch_rotor2, notch_rotor1]

    def set_rotor_positions(self, pos1, pos2, pos3):
        self.rotor_positions = [pos1, pos2, pos3]

    def set_plugboard(self, plugboard):
        self.plugboard = plugboard

    def step_rotors(self):
        if self.rotor_positions[1] == self.notches[1] and self.rotor_positions[2] == self.notches[2]:
            if self.rotor_positions[0] == 'Z':
                self.rotor_positions[0] = 'A'
            else:
                self.rotor_positions[0] = chr(ord(self.rotor_positions[0]) + 1)
        if self.rotor_positions[2] == self.notches[2]:
            if self.rotor_positions[1] == 'Z':
                self.rotor_positions[1] = 'A'
            else:
                self.rotor_positions[1] = chr(ord(self.rotor_positions[1]) + 1)
        if self.rotor_positions[2] == 'Z':
            self.rotor_positions[2] = 'A'
        else:
            self.rotor_positions[2] = chr(ord(self.rotor_positions[2]) + 1)

    def encode_letter(self, letter):

        if letter.islower():
            letter = letter.upper()
        else:
            pass

        # Step rotors
        self.step_rotors()

        # Apply plugboard
        letter = self.plugboard.get(letter, letter)

        # Rotor offsets
        rotor_offset = [ord(self.rotor_positions[0]) - ord('A'), ord(self.rotor_positions[1]) - ord('A'),
                        ord(self.rotor_positions[2]) - ord('A')]
        temp_offset = None

        # Encode through rotors in forward direction (I -> II -> III -> Reflector)
        for i in range(2, -1, -1):
            if i == 1 and rotor_offset[2] != 0:
                temp_offset = rotor_offset[i]
                rotor_offset[i] = rotor_offset[i] - rotor_offset[i+1]
            elif i == 0 and rotor_offset[1] != 0:
                temp_offset = rotor_offset[i]
                rotor_offset[i] = rotor_offset[i] - rotor_offset[i+1]

            letter_idx = ord(letter) - ord('A')
            letter_idx = (letter_idx + rotor_offset[i]) % 26
            letter = chr((ord(self.rotors[i][letter_idx])))

            if temp_offset is not None:
                rotor_offset[i] = temp_offset
                temp_offset = None

        # Reflect through reflector
        letter_idx = ord(letter) - ord('A') - rotor_offset[0]
        letter = self.reflector[letter_idx]

        # Encode through rotors in reverse direction (Reflector -> III -> II -> I)
        for i in range(3):
            if i == 1 and rotor_offset[0] != 0:
                temp_offset = rotor_offset[i]
                rotor_offset[i] = rotor_offset[i] - rotor_offset[i-1]
            elif i == 2 and rotor_offset[1] != 0:
                temp_offset = rotor_offset[i]
                rotor_offset[i] = rotor_offset[i] - rotor_offset[i-1]

            letter_idx = self.rotors[i].index(chr(((ord(letter) - ord('A') + rotor_offset[i]) % 26) + ord('A')))
            letter = chr(letter_idx + ord('A'))

            if temp_offset is not None:
                rotor_offset[i] = temp_offset
                temp_offset = None

        # Offset of last rotor in reverse direction
        letter = chr(((ord(letter) - ord('A') - rotor_offset[2]) % 26) + ord('A'))

        # Apply plugboard
        letter = self.plugboard.get(letter, letter)

        return letter


def enigma(a):
    return a
