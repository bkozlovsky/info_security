import random
import math
import os
from typing import List, Tuple, Dict
import re  # For parsing the private key file

class KnapsackCipher:
    def __init__(self, key_size: int = 8):
        """
        Initialize the Knapsack cipher with a given key size.

        Args:
            key_size: The size of the key (number of elements in the knapsack sequence)
        """
        self.key_size = key_size
        self.private_key = None
        self.public_key = None
        self.n = None
        self.m = None

    def is_prime(self, n: int) -> bool:
        """Check if a number is prime."""
        if n <= 1:
            return False
        if n <= 3:
            return True
        if n % 2 == 0 or n % 3 == 0:
            return False
        i = 5
        while i * i <= n:
            if n % i == 0 or n % (i + 2) == 0:
                return False
            i += 6
        return True

    def find_coprime(self, m: int) -> int:
        """Find a prime number n that is coprime to m."""
        # Start with a random number in the desired range
        n = random.randint(m // 2, m - 1)

        # Find the next prime number
        while not self.is_prime(n) or math.gcd(n, m) != 1:
            n += 1

        return n

    def generate_private_key(self) -> List[int]:
        """
        Generate a superincreasing sequence for the private key.
        In this variant, the first element is 32 and the step range is 8-16.
        """
        private_key = [32]  # Starting with 32 as specified

        for _ in range(1, self.key_size):
            # Generate a random step between 8 and 16
            step = random.randint(8, 16)

            # The next element must be greater than the sum of all previous elements
            next_element = sum(private_key) + step
            private_key.append(next_element)

        return private_key

    def generate_public_key(self, private_key: List[int], n: int, m: int) -> List[int]:
        """
        Generate a public key using the formula: e_i = (d_i * n) mod m.

        Args:
            private_key: The private key (superincreasing sequence)
            n: A prime number that is coprime to m
            m: A modulus greater than the sum of all elements in private_key

        Returns:
            The public key
        """
        return [(d_i * n) % m for d_i in private_key]

    def extended_gcd(self, a: int, b: int) -> Tuple[int, int, int]:
        """
        Extended Euclidean Algorithm to find gcd(a, b) and coefficients x, y such that ax + by = gcd(a, b).

        Returns:
            (gcd, x, y)
        """
        if a == 0:
            return b, 0, 1
        else:
            gcd, x1, y1 = self.extended_gcd(b % a, a)
            x = y1 - (b // a) * x1
            y = x1
            return gcd, x, y

    def mod_inverse(self, a: int, m: int) -> int:
        """
        Find the modular multiplicative inverse of a under modulo m.

        Args:
            a: The number to find the inverse for
            m: The modulus

        Returns:
            The modular multiplicative inverse
        """
        gcd, x, y = self.extended_gcd(a, m)
        if gcd != 1:
            raise Exception("Modular inverse does not exist")
        else:
            return x % m

    def text_to_binary(self, text: str) -> str:
        """
        Convert text to binary representation.

        Args:
            text: The text to convert

        Returns:
            Binary representation of the text
        """
        binary = ""
        for char in text:
            # Convert to binary and remove '0b' prefix
            char_binary = bin(ord(char))[2:].zfill(16)  # Using 16 bits to support Ukrainian characters
            binary += char_binary
        return binary

    def binary_to_text(self, binary: str) -> str:
        """
        Convert binary representation back to text.

        Args:
            binary: The binary representation

        Returns:
            The original text
        """
        text = ""
        # Process 16 bits at a time
        for i in range(0, len(binary), 16):
            chunk = binary[i:i+16]
            if len(chunk) == 16:  # Ensure we have a full chunk
                char_code = int(chunk, 2)
                text += chr(char_code)
        return text

    def encrypt(self, message: str) -> Dict:
        # Початкові налаштування (як раніше)
        self.private_key = self.generate_private_key()
        self.m = sum(self.private_key) + random.randint(1, 100)
        self.n = self.find_coprime(self.m)
        self.public_key = self.generate_public_key(self.private_key, self.n, self.m)

        # Зберігаємо приватний ключ (як раніше)
        with open("private_key.txt", "w") as f:
            f.write(f"Private Key: {self.private_key}\n")
            f.write(f"Modulus (m): {self.m}\n")
            f.write(f"Multiplier (n): {self.n}\n")

        # Конвертуємо повідомлення в бінарний код
        binary = self.text_to_binary(message)

        # Дані для візуалізації
        visualization_data = []
        encrypted_weights = []

        # Обробляємо блоки
        for i in range(0, len(binary), self.key_size):
            block = binary[i:i+self.key_size].zfill(self.key_size)

            # Визначаємо, до якого символу належить цей блок і яка його частина
            char_index = i // 16
            bit_position = (i % 16) // 8  # 0 для першої половини, 1 для другої половини

            if char_index < len(message):
                character = message[char_index]
                part_label = f"Частина {bit_position+1}/2"
            else:
                character = ""
                part_label = ""

            # Дані для візуалізації блока
            block_viz = {
                "block": block,
                "selected_weights": [],
                "weight_sum": 0,
                "character": character,
                "part_label": part_label
            }

            # Обчислюємо суму ваг для цього блока
            weight_sum = 0
            for j in range(len(block)):
                if j < len(self.public_key):
                    if block[j] == '1':
                        weight = self.public_key[j]
                        weight_sum += weight
                        # Додаємо вагу до візуалізації як словник (не кортеж)
                        block_viz["selected_weights"].append({"idx": j, "weight": weight})
                    else:
                        block_viz["selected_weights"].append({"idx": j, "weight": 0})  # Не вибрано

            block_viz["weight_sum"] = weight_sum
            visualization_data.append(block_viz)
            encrypted_weights.append(weight_sum)

        # Створюємо зашифроване повідомлення
        encrypted_message = " ".join(map(str, encrypted_weights))

        return {
            "encrypted_message": encrypted_message,
            "binary_code": binary,
            "weights": encrypted_weights,
            "public_key": self.public_key,
            "visualization_data": visualization_data  # Дані для візуалізації
        }

    def read_private_key_from_file(self) -> Tuple[List[int], int, int]:
        """
        Read the private key, modulus, and multiplier from the file.

        Returns:
            Tuple of (private_key, modulus, multiplier)
        """
        private_key = None
        m = None
        n = None

        try:
            with open("private_key.txt", "r") as f:
                content = f.read()

                # Extract private key
                private_key_match = re.search(r"Private Key: \[(.*?)\]", content)
                if private_key_match:
                    private_key = list(map(int, private_key_match.group(1).split(',')))

                # Extract modulus
                m_match = re.search(r"Modulus \(m\): (\d+)", content)
                if m_match:
                    m = int(m_match.group(1))

                # Extract multiplier
                n_match = re.search(r"Multiplier \(n\): (\d+)", content)
                if n_match:
                    n = int(n_match.group(1))

                if not all([private_key, m, n]):
                    raise ValueError("Could not extract all required values from private key file")

                return private_key, m, n
        except (FileNotFoundError, ValueError) as e:
            raise Exception(f"Error reading private key file: {str(e)}")

    def decrypt(self, encrypted_message: str, public_key: List[int]) -> str:
        """
        Decrypt a message encrypted with the Knapsack cryptosystem.

        Args:
            encrypted_message: The encrypted message (space-separated weights)
            public_key: The public key used for encryption

        Returns:
            The decrypted message
        """
        # Read private key, modulus, and multiplier from file
        private_key, m, n = self.read_private_key_from_file()

        # Parse the encrypted weights
        encrypted_weights = list(map(int, encrypted_message.split()))

        # Calculate the modular multiplicative inverse of n
        n_inverse = self.mod_inverse(n, m)

        # Decrypt each weight to get the binary blocks
        binary = ""

        for weight in encrypted_weights:
            # Convert to the equivalent sum in the superincreasing sequence
            original_sum = (weight * n_inverse) % m

            # Solve the subset sum problem (easy with a superincreasing sequence)
            block = ['0'] * len(private_key)
            for i in range(len(private_key) - 1, -1, -1):
                if original_sum >= private_key[i]:
                    block[i] = '1'
                    original_sum -= private_key[i]

            binary += ''.join(block)

        # Convert binary back to text
        decrypted_message = self.binary_to_text(binary)

        return decrypted_message
