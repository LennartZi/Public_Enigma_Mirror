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
        :param position: position to set the rotor to. Given as capital letter
        """
        if position in self.mapping:
            position = index_from_letter(position)
            self.position = letter_from_index(position)
        else:
            raise ValueError("position not included in mapping")  # This is kinda bad :)
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
        self.calculate_offset()  # updates self.offset after stepping the rotor

    def encrypt_character(self, letter):
        """
        Encrypts the letter, used when entering from the input side.
        :param letter: Position for which we want the encrypted letter, given as a capital character
        :return: Letter after encryption by this rotor
        """
        letter_index = index_from_letter(letter)

        encrypted_letter = self.mapping[letter_index]
        #  Gives us the letter that corresponds to the letter_index position in the rotor map.
        #  This lets us know where we exit the rotor

        return encrypted_letter

    # We need two functions because the way that we enter the rotor (from reflector side or from the input side) matters
    # TODO: rewrite comments to clarify what is going on here

    def encrypt_character_reverse(self, letter):
        """
        Encrypts the letter, used when entering from the reflector side.
        :param letter: Position for which we want the encrypted letter, given as a capital character
        :return: Letter after encryption by this rotor
        """
        encrypted_index = self.mapping.index(letter)
        # this gives us the position on the rotor for our letter. This lets us know where we need to exit the rotor

        encrypted_letter = letter_from_index(encrypted_index)
        # Changes our encrypted index back to a capital letter
        return encrypted_letter

    def calculate_offset(self):
        """
        Calculates the offset (distance from starting position "A") and sets it as offset
        """

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
