class PlayFairCipher:
    def __init__(self):
        pass

    def create_playfair_matrix(self, key):
        key = key.upper().replace("J", "I")

        alphabet = "ABCDEFGHIKLMNOPQRSTUVWXYZ"

        seen = set()
        matrix_chars = []
        for ch in key:
            if ch not in seen and ch in alphabet:
                seen.add(ch)
                matrix_chars.append(ch)

        for ch in alphabet:
            if ch not in seen:
                matrix_chars.append(ch)

        matrix = [matrix_chars[i:i+5] for i in range(0, 25, 5)]
        return matrix

    def find_letter_coords(self, matrix, letter):
        for row in range(5):
            for col in range(5):
                if matrix[row][col] == letter:
                    return row, col
        return None

    def playfair_encrypt(self, plain_text, matrix):
        plain_text = plain_text.upper().replace("J", "I")

        plain_text = ''.join(ch for ch in plain_text if ch.isalpha())

        if len(plain_text) % 2 == 1:
            plain_text += "X"

        encrypted_text = ""
        for i in range(0, len(plain_text), 2):
            a, b = plain_text[i], plain_text[i+1]
            r1, c1 = self.find_letter_coords(matrix, a)
            r2, c2 = self.find_letter_coords(matrix, b)

            if r1 == r2:  
                encrypted_text += matrix[r1][(c1 + 1) % 5]
                encrypted_text += matrix[r2][(c2 + 1) % 5]
            elif c1 == c2:  
                encrypted_text += matrix[(r1 + 1) % 5][c1]
                encrypted_text += matrix[(r2 + 1) % 5][c2]
            else:  
                encrypted_text += matrix[r1][c2]
                encrypted_text += matrix[r2][c1]
        return encrypted_text

    def playfair_decrypt(self, cipher_text, matrix):
        cipher_text = cipher_text.upper()
        decrypted_text = ""
        for i in range(0, len(cipher_text), 2):
            a, b = cipher_text[i], cipher_text[i+1]
            r1, c1 = self.find_letter_coords(matrix, a)
            r2, c2 = self.find_letter_coords(matrix, b)

            if r1 == r2:  
                decrypted_text += matrix[r1][(c1 - 1) % 5]
                decrypted_text += matrix[r2][(c2 - 1) % 5]
            elif c1 == c2:  
                decrypted_text += matrix[(r1 - 1) % 5][c1]
                decrypted_text += matrix[(r2 - 1) % 5][c2]
            else:  
                decrypted_text += matrix[r1][c2]
                decrypted_text += matrix[r2][c1]
        return decrypted_text