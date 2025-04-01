import random
import numpy as np


class SinglePermutationCipher:
    def __init__(self):
        pass

    def encrypt(self, text):
        key = list(range(1, len(text) + 1))
        random.shuffle(key)

        encrypted_text = [""] * len(text)
        for original_index, new_index in enumerate(key, 1):
            encrypted_text[new_index - 1] = text[original_index - 1]

        encrypted_text = "".join(encrypted_text)
        key = "-".join(str(i) for i in key)

        return encrypted_text, key

    def decrypt(self, encrypted_text, key):
        decrypted_text = [""] * len(encrypted_text)
        key = [int(i) for i in key.split("-")]
        for new_index, original_index in enumerate(key):
            decrypted_text[new_index] = encrypted_text[original_index - 1]

        decrypted_text = "".join(decrypted_text)

        return decrypted_text


class RoutePermutationCipher:
    def __init__(self, seed=None):
        self.seed = seed
        if seed is not None:
            random.seed(seed)

    def generate_route(self):
        indices = [0, 1, 2, 3]
        random.shuffle(indices)
        return indices

    def encrypt(self, text):
        text = text.replace(" ", "_")
        blocks = [text[i:i+4].ljust(4, "_") for i in range(0, len(text), 4)]

        route = self.generate_route()
        key = "".join(str(i) for i in route)
        encrypted_text = ""
        for pos in route:
            encrypted_text += "".join(block[pos] for block in blocks)

        return encrypted_text, key

    def decrypt(self, encrypted_text, key):
        # Determine number of blocks
        key = [int(i) for i in key]
        num_blocks = len(encrypted_text) // len(key)
        blocks = [["" for _ in range(len(key))] for _ in range(num_blocks)]

        # Extract segments and place them according to the route
        for i, pos in enumerate(key):
            segment = encrypted_text[i * num_blocks:(i + 1) * num_blocks]
            for j in range(num_blocks):
                blocks[j][pos] = segment[j]

        # Combine blocks and format
        decrypted_text = "".join("".join(block) for block in blocks)
        return decrypted_text.replace("_", " ").strip()


class MultilevelCipher:
    def __init__(self):
        pass

    def encrypt(self, text):
        # Create blocks of 4 characters
        blocks = []
        for i in range(0, len(text), 4):
            blocks.append(text[i : i + 4].ljust(4, "_"))

        # Convert blocks to a matrix of characters
        char_blocks = [[ch for ch in item] for item in blocks]
        matrix = np.array(char_blocks)

        # Get dimensions
        row_length = len(matrix)
        column_length = len(matrix[0])

        # Generate random permutation indices
        row_indices = np.random.permutation(row_length)
        col_indices = np.random.permutation(column_length)

        # Shuffle the matrix
        shuffled_matrix = matrix[row_indices][:, col_indices]

        # Flatten the shuffled matrix in column-major order
        flattened_matrix = shuffled_matrix.flatten(order="F")

        # Join into a single string
        encrypted_text = "".join(flattened_matrix)

        # Create encryption key from the permutation indices
        encryption_key = (
            ",".join(map(str, row_indices)) + "|" + ",".join(map(str, col_indices))
        )

        return encrypted_text, encryption_key

    def decrypt(self, encrypted_text, encryption_key):
        # Parse the encryption key to get row and column indices
        row_indices_str, col_indices_str = encryption_key.split("|")
        row_indices = np.array([int(x) for x in row_indices_str.split(",")])
        col_indices = np.array([int(x) for x in col_indices_str.split(",")])

        # Get dimensions from the key
        row_length = len(row_indices)
        column_length = len(col_indices)

        # Create inverse permutation arrays for unshuffling
        row_inverse = np.zeros(row_length, dtype=int)
        for i, val in enumerate(row_indices):
            row_inverse[val] = i

        col_inverse = np.zeros(column_length, dtype=int)
        for i, val in enumerate(col_indices):
            col_inverse[val] = i

        # Reshape the encrypted text to match the original shuffled matrix
        encrypted_chars = list(encrypted_text)
        reshuffled_matrix = np.array(encrypted_chars).reshape(
            row_length, column_length, order="F"
        )

        # Unshuffle the matrix using the inverse permutation indices
        unshuffled_matrix = reshuffled_matrix[row_inverse][:, col_inverse]

        # Convert back to text and remove padding
        decrypted_text = "".join(["".join(row) for row in unshuffled_matrix]).rstrip(
            "_"
        )

        return decrypted_text
