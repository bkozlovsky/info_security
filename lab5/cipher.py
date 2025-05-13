import random
import math
import base64

class RSACipher:
    def encrypt(self, text):
        """
        Encrypt a text message using RSA encryption.

        Args:
            text: Text message to encrypt

        Returns:
            Tuple of (encrypted_message, public_key e)
        """
        # Hardcoded primes as per requirements
        p = 19
        q = 53

        # Calculate n = p * q
        n = p * q

        # Calculate Euler's totient function: φ(n) = (p-1)(q-1)
        phi = (p - 1) * (q - 1)

        # Choose a public key (e) as a random odd number where 0 < e < n
        # and ensure it's coprime with φ(n)
        e = self._choose_public_key(phi, n)

        # Compute the private exponent d such that: d ≡ e⁻¹ (mod phi(n))
        d = self._modular_inverse(e, phi)

        # Save private key and n to a local file for further access
        self._save_private_key(d, n)

        # Convert text to bytes and then base64 encode
        text_bytes = text.encode('utf-8')

        # Split the bytes into small chunks that fit within n
        chunk_size = 1  # Only processing 1 byte at a time to ensure it's < n
        encrypted_values = []

        for i in range(0, len(text_bytes), chunk_size):
            chunk = text_bytes[i:i+chunk_size]

            # Convert bytes to an integer (ensure it's smaller than n)
            m = int.from_bytes(chunk, byteorder='big')

            if m >= n:
                raise ValueError(f"Byte value {m} is too large for n={n}")

            # Encrypt: c = m^e (mod n)
            c = pow(m, e, n)
            encrypted_values.append(c)

        return encrypted_values, e

    def decrypt(self, encrypted_values, e):
        """
        Decrypt encrypted values using RSA decryption.

        Args:
            encrypted_values: List of encrypted values
            e: Public key used for encryption

        Returns:
            Decrypted text message
        """
        # Read private key and n from file
        d, n = self._read_private_key()

        # Decrypt each value
        decrypted_bytes = bytearray()

        for c in encrypted_values:
            # Decrypt: m = c^d (mod n)
            m = pow(c, d, n)

            # Convert back to bytes
            try:
                byte_val = m.to_bytes((m.bit_length() + 7) // 8, byteorder='big') or b'\x00'
                decrypted_bytes.extend(byte_val)
            except OverflowError:
                # Handle any potential overflow issues
                byte_val = m.to_bytes(1, byteorder='big')
                decrypted_bytes.extend(byte_val)

        # Decode bytes back to text
        try:
            decrypted_text = decrypted_bytes.decode('utf-8')
            return decrypted_text
        except UnicodeDecodeError:
            # If there's an issue with UTF-8 decoding, return the raw bytes
            return decrypted_bytes

    def _gcd(self, a, b):
        """Calculate the greatest common divisor of a and b."""
        while b:
            a, b = b, a % b
        return a

    def _is_coprime(self, a, b):
        """Check if a and b are coprime (gcd(a, b) = 1)."""
        return self._gcd(a, b) == 1

    def _extended_gcd(self, a, b):
        """Extended Euclidean Algorithm to find coefficients s and t such that a*s + b*t = gcd(a, b)."""
        if a == 0:
            return b, 0, 1
        else:
            gcd, x1, y1 = self._extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y

    def _modular_inverse(self, a, m):
        """Calculate the modular inverse of a modulo m."""
        if self._gcd(a, m) != 1:
            raise ValueError("Modular inverse does not exist")
        _, x, _ = self._extended_gcd(a, m)
        return (x % m + m) % m

    def _choose_public_key(self, phi, n):
        """Choose a random odd number e such that 0 < e < n and gcd(e, φ(n)) = 1."""
        # Generate only odd numbers up to n
        candidate_keys = [i for i in range(3, min(phi, 100), 2) if self._is_coprime(i, phi)]

        if not candidate_keys:
            raise ValueError("No suitable public key found")

        return random.choice(candidate_keys)

    def _save_private_key(self, d, n):
        """Save the private key and n to a local file."""
        with open("lab5/files/private_key.txt", "w") as file:
            file.write(f"{d}\n")
            file.write(f"{n}\n")

    def _read_private_key(self):
        """Read the private key and n from the local file."""
        try:
            with open("lab5/files/private_key.txt", "r") as file:
                d = int(file.readline().strip())
                n = int(file.readline().strip())
            return d, n
        except FileNotFoundError:
            raise ValueError("Private key file not found. Encryption must be run first.")
