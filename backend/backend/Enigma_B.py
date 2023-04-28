class EnigmaB:
    def __init__(self, rotor1, rotor2, rotor3, start_pos1, start_pos2, start_pos3, reflector, plugboard=None):
        self.rotors = [rotor1, rotor2, rotor3]
        self.rotor_positions = [start_pos1, start_pos2, start_pos3]
        self.reflector = reflector
        self.plugboard = plugboard or {}

    """ 
    Example-Reflector
    ukw_b = ['Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O', 'K', 'M', 'I', 'E', 'B', 
    'F', 'Z', 'C', 'W', 'V', 'J', 'A', 'T']
                                
    Rotors
    rotor_I = ['E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O', 'W', 'Y', 'H', 'X', 'U', 'S', 'P', 'A',
     'I', 'B', 'R', 'C', 'J']
    
    rotor_II = ['A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W', 'T', 'M', 'C', 'Q', 'G', 'Z', 'N', 'P',
     'Y', 'F', 'V', 'O', 'E']

    rotor_III = ['B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V', 'Z', 'N', 'Y', 'E', 'I', 'W', 'G', 'A',
     'K', 'M', 'U', 'S', 'Q', 'O']
    """

    def set_rotor_positions(self, pos1, pos2, pos3):
        self.rotor_positions = [pos1, pos2, pos3]

    def set_plugboard(self, plugboard):
        self.plugboard = plugboard

    def step_rotors(self):
        if self.rotor_positions[1] == 'Z':
            self.rotor_positions[0] = chr(ord(self.rotor_positions[0]) + 1)
            self.rotor_positions[1] = 'A'
        if self.rotor_positions[2] == 'Z':
            self.rotor_positions[1] = chr(ord(self.rotor_positions[1]) + 1)
            self.rotor_positions[2] = 'A'
        self.rotor_positions[2] = chr(ord(self.rotor_positions[2]) + 1)

    def encode_letter(self, letter):
        # Step rotors before encoding
        self.step_rotors()

        # Apply plugboard
        letter = self.plugboard.get(letter, letter)

        # Encode through rotors in forward direction
        for i in range(3):
            letter_idx = ord(letter) - ord('A')
            rotor_offset = ord(self.rotor_positions[i]) - ord('A')
            letter_idx = (letter_idx + rotor_offset) % 26
            letter = chr((ord(self.rotors[i][letter_idx]) - rotor_offset) % 26 + ord('A'))

        # Reflect through reflector
        letter_idx = ord(letter) - ord('A')
        letter = self.reflector[letter_idx]

        # Encode through rotors in reverse direction
        for i in range(2, -1, -1):
            letter_idx = ord(letter) - ord('A')
            rotor_offset = ord(self.rotor_positions[i]) - ord('A')
            letter_idx = (letter_idx + rotor_offset) % 26
            letter = chr((self.rotors[i].index(chr((letter_idx - rotor_offset) % 26 + ord('A')))) % 26 + ord('A'))

        # Apply plugboard
        letter = self.plugboard.get(letter, letter)

        return letter
