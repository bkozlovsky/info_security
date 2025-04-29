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
