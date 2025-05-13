class LFSRCipher:
    def __init__(self, polynomial, initial_state=None):
        """
        Ініціалізує шифр на основі РСЛЗЗ.

        :param polynomial: Поліном у вигляді списку степенів (від найбільшого до найменшого)
        :param initial_state: Початковий стан регістра (якщо None, заповнюється одиницями)
        """
        self.polynomial = sorted(polynomial, reverse=True)
        self.register_size = max(polynomial)

        # Зберігаємо початковий стан для можливості скидання
        self.initial_state = initial_state

        # Якщо початковий стан не задано, заповнюємо одиницями
        if initial_state is None:
            self.register = [1] * self.register_size
        else:
            # Перевіряємо, що початковий стан правильної довжини
            if len(initial_state) != self.register_size:
                raise ValueError(
                    f"Початковий стан повинен мати довжину {self.register_size}"
                )
            self.register = initial_state[:]

    def _next_bit(self):
        """Генерує наступний біт РСЛЗЗ та оновлює регістр."""
        # Обчислюємо новий біт як XOR вказаних бітів згідно з поліномом
        # Поліном x^10 + x^5 + x^4 + x^2 + 1 означає, що ми беремо біти
        # з позицій 10-1=9, 5-1=4, 4-1=3, 2-1=1 та 0 (зсуви регістра)
        feedback_bits = [
            self.register[self.register_size - p - 1]
            for p in self.polynomial
            if p < self.register_size
        ]

        # Обчислюємо XOR всіх відібраних бітів
        new_bit = 0
        for bit in feedback_bits:
            new_bit ^= bit

        # Зсуваємо регістр вправо (видаляємо останній біт)
        # та вставляємо новий біт на початок
        self.register.pop()
        self.register.insert(0, new_bit)

        return new_bit

    def generate_keystream(self, length):
        """Генерує потік ключів вказаної довжини."""
        return [self._next_bit() for _ in range(length)]

    def encrypt(self, message):
        """
        Шифрує повідомлення, використовуючи РСЛЗЗ як потоковий шифр.

        :param message: Повідомлення у вигляді рядка
        :return: Зашифроване повідомлення у вигляді списку байтів
        """
        # Перевіряємо, чи вхідне повідомлення є рядком
        if isinstance(message, str):
            # Перетворюємо повідомлення у список байтів
            message_bytes = message.encode("utf-8")
        else:
            # Якщо повідомлення вже в байтах, використовуємо його безпосередньо
            message_bytes = message

        # Генеруємо потік ключів потрібної довжини
        keystream_bits = self.generate_keystream(len(message_bytes) * 8)

        # Перетворюємо потік бітів у байти
        keystream_bytes = []
        for i in range(0, len(keystream_bits), 8):
            byte = 0
            for j in range(8):
                if i + j < len(keystream_bits):
                    byte = (byte << 1) | keystream_bits[i + j]
            keystream_bytes.append(byte)

        # Шифруємо повідомлення, застосовуючи XOR до кожного байту
        encrypted_bytes = [
            (message_bytes[i] ^ keystream_bytes[i]) for i in range(len(message_bytes))
        ]

        return encrypted_bytes

    def decrypt(self, encrypted_bytes, reset_state=True, return_bytes=False):
        """
        Розшифровує повідомлення.

        :param encrypted_bytes: Зашифроване повідомлення у вигляді списку байтів
        :param reset_state: Якщо True, регістр буде скинуто до початкового стану
        :param return_bytes: Якщо True, повертає результат як байти, інакше спробує конвертувати в рядок UTF-8
        :return: Розшифроване повідомлення у вигляді рядка або байтів
        """
        # Скидаємо стан регістра, якщо потрібно
        if reset_state:
            self.__init__(self.polynomial, self.initial_state)

        # Генеруємо потік ключів потрібної довжини
        keystream_bits = self.generate_keystream(len(encrypted_bytes) * 8)

        # Перетворюємо потік бітів у байти
        keystream_bytes = []
        for i in range(0, len(keystream_bits), 8):
            byte = 0
            for j in range(8):
                if i + j < len(keystream_bits):
                    byte = (byte << 1) | keystream_bits[i + j]
            keystream_bytes.append(byte)

        # Розшифровуємо повідомлення, застосовуючи XOR до кожного байту
        decrypted_bytes = [
            encrypted_bytes[i] ^ keystream_bytes[i] for i in range(len(encrypted_bytes))
        ]

        # Повертаємо байти або спробуємо конвертувати в рядок
        if return_bytes:
            return bytes(decrypted_bytes)
        else:
            try:
                return bytes(decrypted_bytes).decode("utf-8")
            except UnicodeDecodeError:
                print(
                    "Попередження: Не вдалося декодувати байти як UTF-8. Повертаємо байти."
                )
                return bytes(decrypted_bytes)

    def display_register(self):
        """Виводить поточний стан регістра."""
        return "".join(map(str, self.register))


# Приклад використання
if __name__ == "__main__":
    # Створюємо шифр з поліномом x^10 + x^5 + x^4 + x^2 + 1
    # (індекси 10, 5, 4, 2, 0)
    polynomial = [10, 5, 4, 2, 0]

    # Початковий стан регістра (має бути довжини 10)
    # Не використовуємо всі нулі, оскільки тоді РСЛЗЗ зациклиться на нулях
    initial_state = [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]

    # Ініціалізуємо шифр
    cipher = LFSRCipher(polynomial, initial_state)

    # Повідомлення для шифрування
    message = "Привіт, це тестове повідомлення для шифрування з використанням РСЛЗЗ!"

    print(f"Початковий стан регістра: {cipher.display_register()}")

    # Шифруємо повідомлення
    encrypted = cipher.encrypt(message)
    print(f"Зашифроване повідомлення (байти): {encrypted}")

    # Виводимо зашифроване повідомлення у шістнадцятковому форматі
    hex_encrypted = " ".join([format(b, "02x") for b in encrypted])
    print(f"Зашифроване повідомлення (hex): {hex_encrypted}")

    # Розшифровуємо повідомлення
    decrypted = cipher.decrypt(encrypted)
    print(f"Розшифроване повідомлення: {decrypted}")

    # Перевіряємо, чи збігається розшифроване повідомлення з оригінальним
    assert (
        decrypted == message
    ), "Помилка: розшифроване повідомлення не збігається з оригіналом"
