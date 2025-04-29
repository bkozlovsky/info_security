import random
import numpy as np
import math
import pandas as pd
from typing import Tuple, Dict, List, Optional

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

class VariantCipher:
    def __init__(self,
                 row_markers: Optional[List[str]] = None,
                 col_markers: Optional[List[str]] = None,
                 size: int = 6):

        self.size = size
        self.row_markers = row_markers
        self.col_markers = col_markers

        # Словники для зберігання зв'язків між символами та позиціями
        self.char_to_positions = {}  # Відображає символи на їх позиції в таблиці
        self.position_to_char = {}   # Відображає позиції (рядок, стовпець) на символи

        # Якщо маркери не надані, генеруємо їх
        if row_markers is None or col_markers is None:
            self._generate_markers()
        else:
            if not self._validate_markers(row_markers, col_markers):
                raise ValueError("Маркери рядків та стовпців не повинні мати спільних літер")

        # Завжди генеруємо таблицю випадковим чином
        self._generate_table()

    def _validate_markers(self, row_markers: List[str], col_markers: List[str]) -> bool:
        """Перевіряє, що маркери рядків та стовпців не мають спільних літер."""
        row_letters = set(''.join(row_markers))
        col_letters = set(''.join(col_markers))
        return len(row_letters.intersection(col_letters)) == 0

    def _generate_markers(self):
        """Генерує маркери рядків та стовпців, які не мають спільних літер."""
        # Українські літери для маркерів рядків та стовпців
        all_letters = "АБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ"
        letters = random.sample(all_letters, min(self.size * 4, len(all_letters)))

        # Розділяємо на дві групи для маркерів рядків та стовпців
        midpoint = len(letters) // 2
        row_letters = letters[:midpoint]
        col_letters = letters[midpoint:]

        # Створюємо двобуквені комбінації
        self.row_markers = [row_letters[i] + row_letters[i+1] for i in range(0, len(row_letters) - 1, 2)]
        self.col_markers = [col_letters[i] + col_letters[i+1] for i in range(0, len(col_letters) - 1, 2)]

        # Переконуємося, що маємо достатньо маркерів
        while len(self.row_markers) < self.size:
            self.row_markers.append(self.row_markers[-1] + "1")

        while len(self.col_markers) < self.size:
            self.col_markers.append(self.col_markers[-1] + "1")

    def _generate_table(self):
        """Генерує випадкову таблицю шифрозамін."""
        # Український алфавіт без повторення символів
        alphabet = "АБВГДЕЄЖЗИІЇЙКЛМНОПРСТУФХЦЧШЩЬЮЯ-"
        chars = list(alphabet)
        random.shuffle(chars)  # Перемішуємо символи випадковим чином

        # Створюємо таблицю
        self.table = []
        char_index = 0

        for row in range(self.size):
            row_data = []
            for col in range(self.size):
                if char_index < len(chars):
                    char = chars[char_index]
                    row_data.append(char)

                    # Додаємо до словників відображення
                    if char not in self.char_to_positions:
                        self.char_to_positions[char] = []
                    self.char_to_positions[char].append((row, col))

                    self.position_to_char[(row, col)] = char

                    char_index += 1
                else:
                    # Заповнюємо решту клітинок замінником
                    row_data.append("-")
                    self.position_to_char[(row, col)] = "-"

            self.table.append(row_data)

    def get_table_display(self) -> str:
        """Отримує HTML-представлення таблиці шифрозамін."""
        df = pd.DataFrame(self.table)
        df.columns = self.col_markers
        df.index = self.row_markers

        # Додаємо необхідні стилі CSS
        css_style = """
        <style>
            .cipher-table {
                border-collapse: collapse;
                width: 100%;
            }
            .cipher-table th, .cipher-table td {
                border: 1px solid #dee2e6;
                padding: 8px;
                text-align: center;
                vertical-align: middle;
            }
            .cipher-table thead th {
                background-color: #f8f9fa;
                font-weight: bold;
            }
            .cipher-table tbody th {
                background-color: #f8f9fa;
                font-weight: bold;
            }
        </style>
        """

        # Генеруємо HTML таблиці
        html = df.to_html(
            classes="cipher-table",
            border=1,
            index=True,
            escape=False,
            justify='center'
        )

        return css_style + html

    def encrypt(self, plaintext: str) -> Tuple[str, Dict]:
        """
        Шифрує текст використовуючи варіантний шифр.

        Аргументи:
            plaintext: Текст для шифрування

        Повертає:
            Кортеж, що містить:
                - Зашифрований текст
                - Ключ шифрування (таблиця шифрозамін, маркери та структура оригінального тексту)
        """
        plaintext_upper = plaintext.upper()
        encrypted_parts = []
        original_structure = []
        char_count = 0

        # Зберігаємо структуру вихідного тексту
        for i, char in enumerate(plaintext):
            if char.isspace():
                original_structure.append((i, 'space'))
            else:
                original_structure.append((i, 'char'))
                char_count += 1

        # Шифруємо кожний символ окремо (крім пробілів)
        for char in plaintext_upper:
            if char.isspace():
                continue  # Пропускаємо пробіли при шифруванні

            if char in self.char_to_positions:
                # Отримуємо всі можливі позиції для цього символу
                positions = self.char_to_positions[char]
                # Вибираємо випадкову позицію
                row, col = random.choice(positions)
                row_marker = self.row_markers[row]
                col_marker = self.col_markers[col]

                # Генеруємо всі можливі комбінації окремих літер з маркерів рядків та стовпців
                combinations = []
                for r_letter in row_marker:
                    for c_letter in col_marker:
                        combinations.append(r_letter + c_letter)
                        combinations.append(c_letter + r_letter)

                # Вибираємо випадкову комбінацію
                encrypted_parts.append(random.choice(combinations))
            else:
                # Якщо символ відсутній у таблиці шифрозамін, використовуємо спеціальний маркер
                encrypted_parts.append(f"<{char}>")  # Спеціальний формат для нешифрованих символів

        # Об'єднуємо зашифровані частини пробілами
        encrypted_text = " ".join(encrypted_parts)

        # Ключ шифрування включає таблицю, маркери та оригінальну структуру тексту
        key = {
            "table": self.table,
            "row_markers": self.row_markers,
            "col_markers": self.col_markers,
            "original_structure": original_structure
        }

        return encrypted_text, key

    def decrypt(self, ciphertext: str, key: Dict) -> str:
        """
        Розшифровує текст використовуючи наданий ключ.

        Аргументи:
            ciphertext: Зашифрований текст
            key: Ключ шифрування, що містить таблицю шифрозамін, маркери та структуру оригінального тексту

        Повертає:
            Розшифрований текст з відновленою оригінальною структурою
        """
        # Завантажуємо компоненти ключа
        table = key["table"]
        row_markers = key["row_markers"]
        col_markers = key["col_markers"]
        original_structure = key["original_structure"]

        # Створюємо відображення для розшифрування
        row_marker_letters = {}
        for idx, marker in enumerate(row_markers):
            for letter in marker:
                if letter not in row_marker_letters:
                    row_marker_letters[letter] = []
                row_marker_letters[letter].append(idx)

        col_marker_letters = {}
        for idx, marker in enumerate(col_markers):
            for letter in marker:
                if letter not in col_marker_letters:
                    col_marker_letters[letter] = []
                col_marker_letters[letter].append(idx)

        # Розділяємо зашифрований текст на частини
        parts = ciphertext.split()
        decrypted_chars = []

        for part in parts:
            # Перевіряємо чи це спеціальний маркер для нешифрованих символів
            if part.startswith("<") and part.endswith(">") and len(part) >= 3:
                decrypted_chars.append(part[1:-1])  # Витягуємо символ між < >
                continue

            if len(part) != 2:
                # Якщо не двобуквена частина, залишаємо як є
                decrypted_chars.append(part)
                continue

            first_letter, second_letter = part[0], part[1]
            candidates = []

            # Спробуємо першу літеру як маркер рядка, другу як маркер стовпця
            if first_letter in row_marker_letters and second_letter in col_marker_letters:
                for row in row_marker_letters[first_letter]:
                    for col in col_marker_letters[second_letter]:
                        if 0 <= row < len(table) and 0 <= col < len(table[0]):
                            candidates.append(table[row][col])

            # Спробуємо першу як маркер стовпця, другу як маркер рядка
            if first_letter in col_marker_letters and second_letter in row_marker_letters:
                for col in col_marker_letters[first_letter]:
                    for row in row_marker_letters[second_letter]:
                        if 0 <= row < len(table) and 0 <= col < len(table[0]):
                            candidates.append(table[row][col])

            # Якщо є кандидати, вибираємо перший
            if candidates:
                decrypted_chars.append(candidates[0])
            else:
                # Якщо немає кандидатів, залишаємо як є
                decrypted_chars.append(part)

        # Відновлюємо оригінальну структуру тексту
        result = [""] * len(original_structure)
        char_index = 0

        for i, (pos, type_) in enumerate(original_structure):
            if type_ == 'space':
                result[pos] = " "
            else:
                if char_index < len(decrypted_chars):
                    result[pos] = decrypted_chars[char_index]
                    char_index += 1
                else:
                    result[pos] = "?"  # Заповнювач на випадок помилки

        return "".join(result)
