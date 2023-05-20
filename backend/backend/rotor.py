class Rotor:
    def __init__(self, rotor_mapping, position, notch):
        self.mapping = rotor_mapping
        self.position = position
        self.notch = notch
        self.offset = 0

    def set_position(self, position):
        """
        Sets rotor position to any setting
        """
        if position in self.mapping:
            position = get_alphabet_index(position)
            self.position = get_letter(position)
        else:
            raise ValueError("position not included in mapping")

    def step_rotor(self):
        """
        steps the rotor by one
        """
        # gets the index for the current position
        index = get_alphabet_index(self.position)

        # adds one step to the rotor and checks for a full rotation
        step = index + 1
        if step == 26:
            step = 0

        letter = get_letter(step)

        self.position = letter


def get_alphabet_index(letter):
    """
    Get the index of a letter in the alphabet, where A = 0, B = 1, etc.

    :param letter: A single uppercase letter
    :return: The index of the letter (0-25)
    """
    # letter = letter.upper
    alphabet_index = ord(letter) - ord('A')  # sets A - Z to 0-25
    alphabet_index = alphabet_index % 26  # ensures that we don't overstep the alphabet

    return alphabet_index


def get_letter(index):
    """
    Get the letter for an index in the alphabet, where 0 = A, 1 = B, etc.

    :param index: A number between 0 and 25
    :return: The letter for the given index
    """
    index = index + ord('A')
    letter = chr(index)

    return letter
