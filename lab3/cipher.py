import random


class ModAdditionCipher:
    def __init__(self):
        self.scheme = {
            "А": 0,
            "Б": 1,
            "В": 2,
            "Г": 3,
            "Ґ": 4,
            "Д": 5,
            "Е": 6,
            "Є": 7,
            "Ж": 8,
            "З": 9,
            "И": 10,
            "І": 11,
            "Ї": 12,
            "Й": 13,
            "К": 14,
            "Л": 15,
            "М": 16,
            "Н": 17,
            "О": 18,
            "П": 19,
            "Р": 20,
            "С": 21,
            "Т": 22,
            "У": 23,
            "Ф": 24,
            "Х": 25,
            "Ц": 26,
            "Ч": 27,
            "Ш": 28,
            "Щ": 29,
            "Ь": 30,
            "Ю": 31,
            "Я": 32,
            " ": 33,  # Додаємо пробіл як символ алфавіту
        }
        # Створюємо зворотню схему для розшифрування
        self.reverse_scheme = {v: k for k, v in self.scheme.items()}
        # Довжина схеми (N для операції за модулем)
        self.N = len(self.scheme)

    def encrypt(self, message, key):
        message = message.upper()  # Переводимо в верхній регістр
        key = key.upper()  # Переводимо в верхній регістр

        # Розширюємо ключ, якщо він коротший за повідомлення
        if len(key) < len(message):
            key = (key * (len(message) // len(key) + 1))[: len(message)]

        encrypted = []

        for i in range(len(message)):
            # Пропускаємо символи, яких немає в нашій схемі
            if message[i] not in self.scheme:
                encrypted.append(message[i])
                continue

            p_i = self.scheme[message[i]]
            k_i = self.scheme[key[i]]
            c_i = (p_i + k_i) % self.N
            encrypted.append(self.reverse_scheme[c_i])

        return "".join(encrypted)

    def decrypt(self, encrypted, key):
        encrypted = encrypted.upper()  # Переводимо в верхній регістр
        key = key.upper()  # Переводимо в верхній регістр

        # Розширюємо ключ, якщо він коротший за зашифроване повідомлення
        if len(key) < len(encrypted):
            key = (key * (len(encrypted) // len(key) + 1))[: len(encrypted)]

        decrypted = []

        # Створюємо дані для візуалізації
        visualization = {
            "message_chars": [],
            "message_indices": [],
            "key_chars": [],
            "key_indices": [],
            "encrypted_chars": [],
            "encrypted_indices": [],
        }

        for i in range(len(encrypted)):
            # Пропускаємо символи, яких немає в нашій схемі
            if encrypted[i] not in self.scheme:
                decrypted.append(encrypted[i])
                continue

            c_i = self.scheme[encrypted[i]]
            k_i = self.scheme[key[i]]
            p_i = (c_i + self.N - k_i) % self.N
            decrypted_char = self.reverse_scheme[p_i]
            decrypted.append(decrypted_char)

            # Додаємо до візуалізації
            visualization["message_chars"].append(decrypted_char)
            visualization["message_indices"].append(p_i)
            visualization["key_chars"].append(key[i])
            visualization["key_indices"].append(k_i)
            visualization["encrypted_chars"].append(encrypted[i])
            visualization["encrypted_indices"].append(c_i)

        decrypted_text = "".join(decrypted)

        # Створюємо таблицю візуалізації
        table = self._create_visualization_table(visualization)

        return decrypted_text, table

    def _create_visualization_table(self, visualization):
        # Створюємо таблицю з трьох груп, кожна з яких має два рядки (символ та індекс)
        table_rows = []

        # Перша група: символи розшифрованого повідомлення та їх індекси
        row = "|"
        for char in visualization["message_chars"]:
            row += f" {char} |"
        table_rows.append(row)

        row = "|"
        for idx in visualization["message_indices"]:
            row += f" {idx} |"
        table_rows.append(row)

        # Друга група: символи ключа та їх індекси
        row = "|"
        for char in visualization["key_chars"]:
            row += f" {char} |"
        table_rows.append(row)

        row = "|"
        for idx in visualization["key_indices"]:
            row += f" {idx} |"
        table_rows.append(row)

        # Третя група: символи зашифрованого повідомлення та їх індекси
        row = "|"
        for char in visualization["encrypted_chars"]:
            row += f" {char} |"
        table_rows.append(row)

        row = "|"
        for idx in visualization["encrypted_indices"]:
            row += f" {idx} |"
        table_rows.append(row)

        # Збираємо всі рядки в одну таблицю
        return "\n".join(table_rows)


class AdditiveCipher:
    def __init__(self):
        self.scheme = {
            "А": 0,
            "Б": 1,
            "В": 2,
            "Г": 3,
            "Ґ": 4,
            "Д": 5,
            "Е": 6,
            "Є": 7,
            "Ж": 8,
            "З": 9,
            "И": 10,
            "І": 11,
            "Ї": 12,
            "Й": 13,
            "К": 14,
            "Л": 15,
            "М": 16,
            "Н": 17,
            "О": 18,
            "П": 19,
            "Р": 20,
            "С": 21,
            "Т": 22,
            "У": 23,
            "Ф": 24,
            "Х": 25,
            "Ц": 26,
            "Ч": 27,
            "Ш": 28,
            "Щ": 29,
            "Ь": 30,
            "Ю": 31,
            "Я": 32,
            " ": 33,  # Додаємо пробіл як символ алфавіту
        }
        self.reverse_scheme = {v: k for k, v in self.scheme.items()}
        self.scheme_length = len(self.scheme)

    def encrypt(self, message):
        message = message.upper()

        if not message:
            return "", None

        # Використовуємо довжину схеми як модуль
        m = self.scheme_length

        # Перетворюємо символи повідомлення на індекси
        message_indices = []
        for char in message:
            if char in self.scheme:
                message_indices.append(self.scheme[char])
            else:
                message_indices.append(-1)

        # Шифруємо повідомлення
        encrypted_indices = []

        # Перший символ залишаємо незмінним
        if message_indices:
            encrypted_indices.append(message_indices[0])

        # Використовуємо індекси попередніх символів для шифрування
        for i in range(1, len(message_indices)):
            if message_indices[i] != -1 and encrypted_indices[i - 1] != -1:
                # Формула шифрування: X_i+1 = (X_i + X_i-1) mod m
                encrypted_index = (message_indices[i] + encrypted_indices[i - 1]) % m
                encrypted_indices.append(encrypted_index)
            else:
                encrypted_indices.append(message_indices[i])

        # Перетворюємо зашифровані індекси назад у символи
        encrypted_message = ""
        for idx in encrypted_indices:
            if idx != -1:
                encrypted_message += self.reverse_scheme.get(idx, "?")
            else:
                encrypted_message += "?"

        return (encrypted_message, m)

    def decrypt(self, encrypted_message, m):
        encrypted_message = encrypted_message.upper()

        if not encrypted_message:
            return ""

        # Перетворюємо символи зашифрованого повідомлення на індекси
        encrypted_indices = []
        for char in encrypted_message:
            if char in self.scheme:
                encrypted_indices.append(self.scheme[char])
            else:
                encrypted_indices.append(-1)

        # Розшифровуємо повідомлення
        decrypted_indices = []

        # Перший символ залишаємо незмінним
        if encrypted_indices:
            decrypted_indices.append(encrypted_indices[0])

        # Використовуємо формулу дешифрування для інших символів
        for i in range(1, len(encrypted_indices)):
            if encrypted_indices[i] != -1 and encrypted_indices[i - 1] != -1:
                # Формула дешифрування: X_i = (C_i - C_i-1 + m) % m
                decrypted_index = (
                    encrypted_indices[i] - encrypted_indices[i - 1] + m
                ) % m
                decrypted_indices.append(decrypted_index)
            else:
                decrypted_indices.append(encrypted_indices[i])

        # Перетворюємо розшифровані індекси назад у символи
        decrypted_message = ""
        for idx in decrypted_indices:
            if idx != -1:
                decrypted_message += self.reverse_scheme.get(idx, "?")
            else:
                decrypted_message += "?"

        return decrypted_message
