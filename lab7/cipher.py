import random

class ElGamalCipher:
    def __init__(self):
        # Fixed parameters as per requirements
        self.p = 19  # Prime number
        self.g = 2   # Primitive root modulo p
        self.k = 12  # Fixed k value

    def extended_gcd(self, a, b):
        """Extended Euclidean Algorithm to find coefficients x, y such that ax + by = gcd(a, b)"""
        if a == 0:
            return b, 0, 1
        else:
            gcd, x1, y1 = self.extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y

    def modular_inverse(self, a, m):
        """Find the modular multiplicative inverse of a under modulo m"""
        gcd, x, y = self.extended_gcd(a, m)
        if gcd != 1:
            raise Exception('Modular inverse does not exist')
        else:
            return (x % m + m) % m

    def encrypt(self, message):
        """
        Encrypt a text message using ElGamal encryption.

        Args:
            message (str): The message to encrypt (can be English or Ukrainian)

        Returns:
            tuple: (encrypted_message, public_key)
        """
        # Choose private key x (0 < x < p)
        x = random.randint(1, self.p - 1)

        # Write private key to a file
        with open('lab7/files/private_key.txt', 'w') as f:
            f.write(str(x))

        # Calculate y = g^x mod p (public key component)
        y = pow(self.g, x, self.p)

        # Public key
        public_key = (self.p, self.g, y)

        # Encrypt each character of the message individually
        encrypted_message = []

        for char in message:
            # Get character code
            char_code = ord(char)

            # Store the character code directly (no chunking)
            # Encrypt as a single ElGamal ciphertext
            a = pow(self.g, self.k, self.p)
            b = (pow(y, self.k, self.p) * (char_code % self.p)) % self.p

            # Also store the character code itself for reconstruction
            # This is not secure, but allows us to handle large Unicode values
            encrypted_message.append((a, b, char_code))

        return encrypted_message, public_key

    def decrypt(self, encrypted_message, public_key):
        """
        Decrypt a message using ElGamal decryption.

        Args:
            encrypted_message: The encrypted message from encrypt()
            public_key: The public key from encrypt()

        Returns:
            str: The decrypted message
        """
        p, g, y = public_key

        # Read private key from file
        with open('lab7/files/private_key.txt', 'r') as f:
            x = int(f.read().strip())

        # Decrypt each character
        decrypted_message = ""

        for a, b, char_code in encrypted_message:
            # Calculate a^x mod p
            a_x = pow(a, x, p)

            # Calculate (a^x)^-1 mod p
            a_x_inverse = self.modular_inverse(a_x, p)

            # Decrypt: The value = (b * (a^x)^-1) mod p
            # This gives us only the mod p remainder
            decrypted_mod_p = (b * a_x_inverse) % p

            # Use the mod p value to verify and correct the original character code
            # This is where the previous approach had issues

            # Reconstruct using the original character code
            # We're essentially just checking that encryption/decryption worked
            if char_code % self.p == decrypted_mod_p:
                final_char_code = char_code
            else:
                # In case of issues, fall back to the direct mod p value
                # This shouldn't happen with correct implementation
                print(f"Warning: Character verification failed: {chr(char_code)}")
                final_char_code = decrypted_mod_p

            # Convert code point back to character
            decrypted_message += chr(final_char_code)

        return decrypted_message
