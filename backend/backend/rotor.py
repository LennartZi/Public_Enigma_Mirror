class Rotor:
    def __init__(self, rotor_mapping, position, notch):
        self.mapping = rotor_mapping
        self.position = position
        self.notch = notch
        self.offset = 0
        self.calculate_offset()

    def set_position(self, position):
        """
        Sets rotor position to any setting
        """
        if position in self.mapping:
            position = index_from_letter(position)
            self.position = letter_from_index(position)
        else:
            raise ValueError("position not included in mapping")
        self.calculate_offset()

    def step_rotor(self):
        """
        steps the rotor by one
        """
        # gets the index for the current position
        index = index_from_letter(self.position)

        # adds one step to the rotor and checks for a full rotation
        step = index + 1
        if step == 26:
            step = 0

        letter = letter_from_index(step)

        self.position = letter
        self.calculate_offset()

    def encrypt_character(self, position_letter):
        """
        :param position_letter: Position for which we want the encrypted letter, given as a capital character
        :return: Letter after encryption by this rotor
        """
        offset_index = index_from_letter(position_letter)
        # current_position = index_from_letter(self.position)

        adjusted_index = offset_index # current_position

        encrypted_letter = self.mapping[adjusted_index]

        return encrypted_letter

    def calculate_offset(self):
        position_index = index_from_letter(self.position)

        offset = position_index

        self.offset = offset


def index_from_letter(letter):
    """
    Get the index of a letter in the alphabet, where A = 0, B = 1, etc.

    :param letter: A single uppercase letter
    :return: The index of the letter (0-25)
    """
    letter = letter.upper()

    # Calculate the index of the letter in the alphabet
    letter_index = ord(letter) - ord('A')

    return letter_index


def letter_from_index(index):
    """
    Get the letter for an index in the alphabet, where 0 = A, 1 = B, etc.

    :param index: A number between 0 and 25
    :return: The letter for the given index
    """
    index = index + ord('A')
    letter = chr(index)

    return letter
