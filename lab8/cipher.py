import os
import math

class HashFunctions:
    def __init__(self):
        pass

    # 1. Checksum parity word
    def checksum_parity(self, data, blocks=4):
        """
        Splits data into specified number of blocks and calculates parity for each block.

        Args:
            data (bytes): Data to hash
            blocks (int): Number of blocks to split data into

        Returns:
            str: Hexadecimal hash value
        """
        if not data:
            return "0" * blocks  # Return zeros for empty data

        # Ensure data is bytes
        if isinstance(data, str):
            data = data.encode('utf-8')

        # Calculate block size, ensuring at least 1 byte per block
        block_size = max(1, len(data) // blocks)
        remainder = len(data) % blocks

        checksums = []

        for i in range(blocks):
            # Calculate start and end indices for this block
            start = i * block_size
            end = start + block_size

            # Add an extra byte to early blocks if data doesn't divide evenly
            if i < remainder:
                end += 1

            # Handle the case where we're at the end of data
            if i == blocks - 1:
                end = len(data)

            # Extract the block
            block = data[start:end]

            # Calculate parity by XORing all bytes in the block
            parity = 0
            for byte in block:
                parity ^= byte

            checksums.append(parity)

        # Convert to hex string
        result = ''.join(f'{c:02x}' for c in checksums)
        return result

    # 2. Mid-Square hashing
    def mid_square_hash(self, data, digits_to_extract=(0, 1)):
        """
        Implements mid-square hashing.

        Args:
            data (str or bytes): Data to hash
            digits_to_extract (tuple): Which digits to extract from the squared value

        Returns:
            int: Hash value
        """
        if not data:
            return 0

        # Convert data to integer
        if isinstance(data, str):
            data = data.encode('utf-8')

        # Sum all bytes to get a single number
        value = sum(data)

        # Square the value
        squared = value * value

        # Convert to string and ensure it has enough digits
        squared_str = str(squared).zfill(max(digits_to_extract) + 1)

        # Extract the specified digits
        extracted = ''.join(squared_str[i] for i in digits_to_extract if i < len(squared_str))

        # Convert back to integer
        if extracted:
            return int(extracted)
        return 0

    # 3. Modular hashing
    def modular_hash(self, data, mod=17):
        """
        Calculates hash using modular arithmetic.

        Args:
            data (str or bytes): Data to hash
            mod (int): Modulus value

        Returns:
            int: Hash value
        """
        if not data:
            return 0

        # Convert data to bytes
        if isinstance(data, str):
            data = data.encode('utf-8')

        # Calculate hash by summing bytes and taking modulo
        hash_value = sum(data) % mod
        return hash_value

    # 4. Method of converting number system
    def number_system_conversion(self, data, p=2, q=4):
        """
        Converts data from base P to base Q.

        Args:
            data (str or bytes): Data to hash
            p (int): Source base
            q (int): Target base

        Returns:
            int: Hash value
        """
        if not data:
            return 0

        # Convert data to bytes
        if isinstance(data, str):
            data = data.encode('utf-8')

        # Convert the data to a binary string
        binary = ''.join(format(byte, '08b') for byte in data)

        # Interpret binary as base-p number and convert to base-q
        # Here we're interpreting each bit as a base-p digit
        decimal_value = int(binary, p)

        # Convert to base-q - we'll return as a decimal for simplicity
        # But represent the value as if it were in base-q
        return decimal_value

    # 5. Folding method
    def folding_hash(self, data, address_size=5):
        """
        Implements folding method for hashing.

        Args:
            data (str or bytes): Data to hash
            address_size (int): Size of the hash address in digits

        Returns:
            int: Hash value
        """
        if not data:
            return 0

        # Convert data to bytes
        if isinstance(data, str):
            data = data.encode('utf-8')

        # Determine segment size based on address_size
        segment_size = max(1, len(data) // 4)  # Divide into ~4 segments
        max_value = 10 ** address_size - 1  # Maximum value with address_size digits

        # Process data in segments
        hash_value = 0
        for i in range(0, len(data), segment_size):
            segment = data[i:i+segment_size]
            # Sum the bytes in this segment
            segment_value = sum(segment)
            # Add to the hash value
            hash_value = (hash_value + segment_value) % max_value

        return hash_value

    # Common methods for both text and file
    def hash_text(self, text, hash_function='checksum'):
        """
        Calculates hash of a text using the specified hash function.

        Args:
            text (str): Text to hash
            hash_function (str): Name of the hash function to use

        Returns:
            Hash value
        """
        if hash_function == 'checksum':
            return self.checksum_parity(text)
        elif hash_function == 'mid_square':
            return self.mid_square_hash(text)
        elif hash_function == 'modular':
            return self.modular_hash(text)
        elif hash_function == 'number_system':
            return self.number_system_conversion(text)
        elif hash_function == 'folding':
            return self.folding_hash(text)
        else:
            raise ValueError(f"Unknown hash function: {hash_function}")

    def hash_file(self, file_path, hash_function='checksum'):
        """
        Calculates hash of a file using the specified hash function.

        Args:
            file_path (str): Path to the file
            hash_function (str): Name of the hash function to use

        Returns:
            Hash value
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, 'rb') as f:
            data = f.read()

        return self.hash_text(data, hash_function)

    def verify_integrity(self, original_data, hash_value, hash_function='checksum'):
        """
        Verifies the integrity of data by comparing its hash with a provided hash value.

        Args:
            original_data (str or bytes): Data to verify
            hash_value: Expected hash value
            hash_function (str): Name of the hash function to use

        Returns:
            bool: True if integrity is verified, False otherwise
        """
        current_hash = self.hash_text(original_data, hash_function)
        return current_hash == hash_value
