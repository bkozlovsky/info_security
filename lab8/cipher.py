import os
import math

class HashFunctions:
    def __init__(self):
        pass

    # 1. Checksum parity word
    def checksum_parity(self, data, blocks=4, salt=None):
        """
        Splits data into specified number of blocks and calculates parity for each block.

        Args:
            data (bytes): Data to hash
            blocks (int): Number of blocks to split data into
            salt (bytes): Optional salt for additional security

        Returns:
            str: Hexadecimal hash value
        """
        if not data:
            return "0" * blocks

        # Ensure data is bytes
        if isinstance(data, str):
            data = data.encode('utf-8')

        # Add salt if provided
        if salt:
            if isinstance(salt, str):
                salt = salt.encode('utf-8')
            data = salt + data

        # Add position-dependent processing
        block_size = max(1, len(data) // blocks)
        remainder = len(data) % blocks

        checksums = []

        for i in range(blocks):
            start = i * block_size
            end = start + block_size

            if i < remainder:
                end += 1

            if i == blocks - 1:
                end = len(data)

            block = data[start:end]

            # Enhanced parity calculation with position weighting
            parity = 0
            for j, byte in enumerate(block):
                # Add position-dependent transformation
                transformed_byte = (byte * (j + 1)) & 0xFF
                # Rotate bits based on block index
                rotated = ((transformed_byte << (i % 8)) | (transformed_byte >> (8 - (i % 8)))) & 0xFF
                parity ^= rotated

            # Mix with block index to prevent block reordering attacks
            parity = (parity + i * 31) & 0xFF
            checksums.append(parity)

        # Final mixing step - combine all checksums
        final_checksum = 0
        for i, cs in enumerate(checksums):
            final_checksum = (final_checksum * 33 + cs) & 0xFFFFFFFF

        # Include final checksum in result for avalanche effect
        result = ''.join(f'{c:02x}' for c in checksums)
        result += f'{final_checksum:08x}'

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

    def verify_integrity(self, original_data, hash_value, hash_function_name):
        hash_function = getattr(self, hash_function_name)
        if hash_function_name == "checksum_parity":
            calculated_hash = hash_function(original_data, blocks=4)
            return hash_value == calculated_hash
        elif hash_function_name == "folding_hash":
            calculated_hash = hash_function(original_data, address_size=5)
            return hash_value == calculated_hash
        elif hash_function_name == "modular_hash":
            calculated_hash = hash_function(original_data, mod=17)
            return hash_value == calculated_hash
        elif hash_function_name == "number_system_conversion":
            calculated_hash = hash_function(original_data, p=2, q=4)
            return hash_value == calculated_hash
        elif hash_function_name == "mid_square_hash":
            calculated_hash = hash_function(original_data, digits_to_extract=(0, 1))
            return hash_value == calculated_hash
