from Enigma_B import EnigmaB


def enigma(a):
    return a


if __name__ == '__main__':
    ukw_b = ['Y', 'R', 'U', 'H', 'Q', 'S', 'L', 'D', 'P', 'X', 'N', 'G', 'O', 'K', 'M', 'I', 'E', 'B',
             'F', 'Z', 'C', 'W', 'V', 'J', 'A', 'T']

    rotor_I = ['E', 'K', 'M', 'F', 'L', 'G', 'D', 'Q', 'V', 'Z', 'N', 'T', 'O', 'W', 'Y', 'H', 'X', 'U', 'S', 'P', 'A',
               'I', 'B', 'R', 'C', 'J']

    rotor_II = ['A', 'J', 'D', 'K', 'S', 'I', 'R', 'U', 'X', 'B', 'L', 'H', 'W', 'T', 'M', 'C', 'Q', 'G', 'Z', 'N', 'P',
                'Y', 'F', 'V', 'O', 'E']

    rotor_III = ['B', 'D', 'F', 'H', 'J', 'L', 'C', 'P', 'R', 'T', 'X', 'V', 'Z', 'N', 'Y', 'E', 'I', 'W', 'G', 'A',
                 'K', 'M', 'U', 'S', 'Q', 'O']

    enigma_b = EnigmaB(rotor_I, rotor_II, rotor_III, "A", "A", "A", ukw_b)

    # loop for encryption
    while True:
        # Input of a letter
        letter = input('Insert a letter: ')

        # Check if input is a letter
        if len(letter) != 1 or not letter.isalpha():
            print('Only one letter please')
            continue

        # Encryption of letter
        encrypted_letter = enigma_b.encode_letter(letter.upper())
        print(f'Encrypted letter: {encrypted_letter}')
