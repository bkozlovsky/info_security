import random
import numpy as np
import math

class PolybianSquare:
    def __init__(self, alphabet=None):
        """
        Ініціалізує Полібіанський квадрат.

        :param alphabet: Алфавіт для таблиці. Якщо None, використовується стандартний алфавіт.
        """
        # Якщо алфавіт не заданий, використовуємо український алфавіт і цифри
        if alphabet is None:
            self.alphabet = list("АБВГҐДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ")
        else:
            self.alphabet = list(alphabet)

    def generate_key(self):
        """
        Генерує випадкову перестановку алфавіту для ключа шифрування.

        :return: Двовимірний масив-ключ (таблиця шифрозамін).
        """
        # Копіюємо та перемішуємо алфавіт
        shuffled_alphabet = self.alphabet.copy()
        random.shuffle(shuffled_alphabet)

        # Визначаємо розміри таблиці
        size = int(np.ceil(np.sqrt(len(shuffled_alphabet))))

        # Створюємо таблицю
        key = []
        for i in range(size):
            row = []
            for j in range(size):
                idx = i * size + j
                if idx < len(shuffled_alphabet):
                    row.append(shuffled_alphabet[idx])
                else:
                    # Якщо символів недостатньо для заповнення таблиці, додаємо пробіл
                    row.append(" ")
            key.append(row)

        return key

    def encrypt(self, plaintext):
        """
        Шифрує текст за допомогою Полібіанського квадрата.

        :param plaintext: Текст для шифрування.
        :return: Кортеж (зашифрований текст, ключ шифрування).
        """
        # Генеруємо ключ
        key = self.generate_key()

        # Перетворюємо текст на верхній регістр
        plaintext = plaintext.upper()

        ciphertext = ""
        for char in plaintext:
            # Пропускаємо символи, яких немає в алфавіті
            if char not in self.alphabet and char != " ":
                ciphertext += char
                continue

            # Знаходимо координати символу в таблиці
            for i, row in enumerate(key):
                if char in row:
                    j = row.index(char)
                    # Додаємо координати як символи (i+1, j+1)
                    ciphertext += f"{i+1}{j+1}"
                    break
            # Додаємо пробіл, якщо символ - пробіл
            if char == " ":
                ciphertext += " "

        return ciphertext, key

    def decrypt(self, ciphertext, key):
        """
        Розшифровує текст, зашифрований Полібіанським квадратом.

        :param ciphertext: Зашифрований текст.
        :param key: Ключ шифрування (таблиця шифрозамін).
        :return: Розшифрований текст.
        """
        plaintext = ""
        i = 0

        while i < len(ciphertext):
            if ciphertext[i] == " ":
                plaintext += " "
                i += 1
                continue

            # Перевіряємо, чи є наступні два символи координатами
            if i + 1 < len(ciphertext) and ciphertext[i].isdigit() and ciphertext[i+1].isdigit():
                row = int(ciphertext[i]) - 1
                col = int(ciphertext[i+1]) - 1

                # Перевіряємо, чи коректні координати
                if 0 <= row < len(key) and 0 <= col < len(key[0]):
                    plaintext += key[row][col]
                else:
                    # Якщо координати некоректні, додаємо їх як символи
                    plaintext += ciphertext[i:i+2]

                i += 2
            else:
                # Якщо це не координати, додаємо символ без зміни
                plaintext += ciphertext[i]
                i += 1

        return plaintext

    def print_key(self, key):
        """
        Виводить ключ (таблицю) у зручному форматі.

        :param key: Ключ шифрування (двовимірний масив).
        """
        print("Таблиця ключа:")
        print("   " + " ".join(f"{i+1}" for i in range(len(key[0]))))
        for i, row in enumerate(key):
            print(f"{i+1}  " + " ".join(row))

class HillCipher:
    def __init__(self, block_size=3):
        # Український алфавіт і відповідні числа, додаємо пробіл
        self.alphabet = {
            "А": 0, "Б": 1, "В": 2, "Г": 3, "Ґ": 4, "Д": 5,
            "Е": 6, "Є": 7, "Ж": 8, "З": 9, "И": 10, "І": 11,
            "Ї": 12, "Й": 13, "К": 14, "Л": 15, "М": 16,
            "Н": 17, "О": 18, "П": 19, "Р": 20, "С": 21,
            "Т": 22, "У": 23, "Ф": 24, "Х": 25, "Ц": 26,
            "Ч": 27, "Ш": 28, "Щ": 29, "Ь": 30, "Ю": 31, "Я": 32,
            " ": 33  # Додаємо пробіл як символ алфавіту
        }

        # Інвертований словник для перетворення чисел назад у символи
        self.reverse_alphabet = {v: k for k, v in self.alphabet.items()}

        # Модуль - довжина алфавіту
        self.modulus = len(self.alphabet)

        # Розмір блоку
        self.block_size = block_size

    # Розширений алгоритм Евкліда для знаходження мультиплікативного оберненого
    def modular_inverse(self, a, m):
        g, x, y = self.extended_gcd(a % m, m)
        if g != 1:
            raise Exception('Модульний обернений не існує')
        else:
            return x % m

    # Розширений алгоритм Евкліда
    def extended_gcd(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

    # Обчислення детермінанта матриці
    def determinant(self, matrix):
        n = len(matrix)

        if n == 1:
            return matrix[0][0] % self.modulus

        if n == 2:
            return (matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]) % self.modulus

        det = 0
        for c in range(n):
            # Обчислюємо алгебраїчне доповнення
            submatrix = [row[:c] + row[c+1:] for row in matrix[1:]]
            sign = (-1) ** c

            # Рекурсивно обчислюємо детермінант підматриці
            sub_det = self.determinant(submatrix)

            # Додаємо до загального детермінанту
            det = (det + sign * matrix[0][c] * sub_det) % self.modulus

        return det

    # Обчислення оберненої матриці за модулем
    def inverse_matrix(self, matrix):
        n = len(matrix)

        # Обчислюємо детермінант
        det = self.determinant(matrix)

        # Перевіряємо, чи існує обернена матриця
        try:
            inverse_det = self.modular_inverse(det, self.modulus)
        except:
            raise Exception("Обернена матриця не існує")

        # Для матриці 2x2
        if n == 2:
            result = [
                [(matrix[1][1] * inverse_det) % self.modulus, (-matrix[0][1] * inverse_det) % self.modulus],
                [(-matrix[1][0] * inverse_det) % self.modulus, (matrix[0][0] * inverse_det) % self.modulus]
            ]
            return result

        # Для матриці 3x3 і більше
        cofactors = []
        for r in range(n):
            cofactor_row = []
            for c in range(n):
                # Обчислюємо мінор
                minor = [row[:c] + row[c+1:] for row in (matrix[:r] + matrix[r+1:])]
                minor_det = self.determinant(minor)

                # Знак алгебраїчного доповнення
                sign = (-1) ** (r + c)

                # Алгебраїчне доповнення
                cofactor_row.append((sign * minor_det * inverse_det) % self.modulus)
            cofactors.append(cofactor_row)

        # Транспонуємо матрицю алгебраїчних доповнень
        result = [[cofactors[c][r] for c in range(n)] for r in range(n)]

        return result

    # Генерація випадкової матриці шифрування та оберненої матриці
    def generate_key_matrix(self):
        while True:
            try:
                # Створюємо випадкову матрицю
                encryption_matrix = [[random.randint(1, self.modulus - 1) for _ in range(self.block_size)] for _ in range(self.block_size)]

                # Обчислюємо детермінант
                det = self.determinant(encryption_matrix)

                # Перевіряємо, чи det і модуль взаємно прості
                if math.gcd(int(det), self.modulus) == 1:
                    # Обчислюємо обернену матрицю
                    decryption_matrix = self.inverse_matrix(encryption_matrix)
                    return encryption_matrix, decryption_matrix
            except Exception:
                # Якщо обернена матриця не існує, генеруємо нову матрицю
                continue

    # Перетворення тексту в числа
    def text_to_numbers(self, text):
        numbers = []
        for char in text:
            if char in self.alphabet:
                numbers.append(self.alphabet[char])
            else:
                # Пропускаємо символи, яких немає в алфавіті
                continue
        return numbers

    # Перетворення чисел назад у текст
    def numbers_to_text(self, numbers):
        text = ""
        for number in numbers:
            text += self.reverse_alphabet[number % self.modulus]
        return text

    # Множення вектора на матрицю за модулем
    def multiply_block(self, block, matrix):
        result = []
        for i in range(len(matrix)):
            sum_val = 0
            for j in range(len(block)):
                sum_val += block[j] * matrix[i][j]
            result.append(sum_val % self.modulus)
        return result

    # Шифрування тексту
    def encrypt(self, plaintext):
        # Перетворюємо текст в числа
        numbers = self.text_to_numbers(plaintext)

        # Визначаємо кількість символів доповнення
        padding_length = self.block_size - (len(numbers) % self.block_size)
        if padding_length == self.block_size:
            padding_length = 0  # Якщо довжина кратна розміру блоку, доповнення не потрібне

        # Додаємо символи доповнення, якщо потрібно
        if padding_length > 0:
            padding_value = padding_length  # Використовуємо кількість доповнень як значення
            for _ in range(padding_length):
                numbers.append(padding_value)

        # Генеруємо ключову матрицю та обернену матрицю
        encryption_matrix, decryption_matrix = self.generate_key_matrix()

        # Розбиваємо на блоки і шифруємо
        encrypted_numbers = []
        for i in range(0, len(numbers), self.block_size):
            block = numbers[i:i + self.block_size]
            encrypted_block = self.multiply_block(block, encryption_matrix)
            encrypted_numbers.extend(encrypted_block)

        # Перетворюємо зашифровані числа назад у текст
        encrypted_text = self.numbers_to_text(encrypted_numbers)

        return (encrypted_text, encrypted_numbers), encryption_matrix, decryption_matrix

    # Розшифрування тексту
    def decrypt(self, encrypted_data, decryption_matrix):
        encrypted_text, encrypted_numbers = encrypted_data

        # Розбиваємо на блоки і розшифровуємо
        decrypted_numbers = []
        for i in range(0, len(encrypted_numbers), self.block_size):
            block = encrypted_numbers[i:i + self.block_size]
            decrypted_block = self.multiply_block(block, decryption_matrix)
            decrypted_numbers.extend(decrypted_block)

        # Видаляємо доповнення, якщо воно є
        if len(decrypted_numbers) > 0:
            # Перевіряємо останній символ
            last_value = decrypted_numbers[-1]

            # Перевіряємо, чи це значення доповнення
            if 0 < last_value < self.block_size:
                # Перевіряємо всі символи доповнення
                is_padding = True
                for i in range(1, last_value + 1):
                    if len(decrypted_numbers) - i < 0 or decrypted_numbers[-i] != last_value:
                        is_padding = False
                        break

                # Якщо це доповнення, видаляємо його
                if is_padding:
                    decrypted_numbers = decrypted_numbers[:-last_value]

        # Перетворюємо розшифровані числа назад у текст
        decrypted_text = self.numbers_to_text(decrypted_numbers)

        return decrypted_text
