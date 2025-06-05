import itertools
from collections import Counter
import math

class FrequencySubstitutionCipher:
    def __init__(self):
        # Частоти літер англійського алфавіту (відсортовані за спаданням)
        english_freq = [
            ('e', 0.1251), ('t', 0.0925), ('a', 0.0804), ('o', 0.0760),
            ('i', 0.0726), ('n', 0.0709), ('s', 0.0654), ('r', 0.0612),
            ('h', 0.0549), ('l', 0.0414), ('d', 0.0399), ('c', 0.0306),
            ('u', 0.0271), ('m', 0.0253), ('f', 0.0230), ('p', 0.0200),
            ('g', 0.0196), ('w', 0.0192), ('y', 0.0173), ('b', 0.0154),
            ('v', 0.0099), ('k', 0.0067), ('x', 0.0019), ('j', 0.0016),
            ('q', 0.0011), ('z', 0.0007)
        ]

        # Частоти літер українського алфавіту (відсортовані за спаданням)
        # Видаляємо пробіл з початку, щоб уникнути конфлікту
        ukrainian_freq = [
            ('о', 0.090), ('е', 0.072), ('а', 0.062),
            ('і', 0.062), ('н', 0.053), ('т', 0.053), ('с', 0.045),
            ('р', 0.040), ('в', 0.038), ('л', 0.035), ('к', 0.028),
            ('м', 0.026), ('д', 0.025), ('п', 0.023), ('у', 0.021),
            ('я', 0.018), ('з', 0.016), ('и', 0.016), ('б', 0.014),
            ('ь', 0.014), ('г', 0.013), ('ч', 0.012), ('й', 0.010),
            ('х', 0.009), ('ж', 0.007), ('ю', 0.006), ('ш', 0.006),
            ('ц', 0.004), ('щ', 0.003), ('є', 0.003), ('ф', 0.002)
        ]

        # Створюємо мапінг для шифрування
        self.encrypt_map = {}
        self.decrypt_map = {}

        # Співставляємо літери за частотою використання
        for i, (eng_char, _) in enumerate(english_freq):
            if i < len(ukrainian_freq):
                ukr_char = ukrainian_freq[i][0]
                self.encrypt_map[eng_char] = ukr_char
                self.decrypt_map[ukr_char] = eng_char

        # Окремо обробляємо пробіл - використовуємо невикористану українську літеру
        unused_ukrainian_chars = [char for char, _ in ukrainian_freq if char not in self.decrypt_map]

        if unused_ukrainian_chars:
            # Використовуємо першу невикористану літеру для пробілу
            space_char = unused_ukrainian_chars[0]
            self.encrypt_map[' '] = space_char
            self.decrypt_map[space_char] = ' '
        else:
            # Якщо всі літери використані, додаємо спеціальний символ
            # (цього не повинно статися з поточними частотами)
            self.encrypt_map[' '] = '§'  # спеціальний символ для пробілу
            self.decrypt_map['§'] = ' '

        # Показуємо мапінг для розуміння
        print("Мапінг шифрування (англійська -> українська):")
        print("-" * 50)
        for eng, ukr in sorted(self.encrypt_map.items()):
            eng_display = "'пробіл'" if eng == ' ' else f"'{eng}'"
            ukr_display = "'пробіл'" if ukr == ' ' else f"'{ukr}'"
            print(f"{eng_display:>8} -> {ukr_display}")

        # Показуємо невикористані українські літери
        remaining_ukrainian = [char for char, _ in ukrainian_freq if char not in self.decrypt_map]
        if remaining_ukrainian:
            print(f"\nНевикористані українські літери: {', '.join(remaining_ukrainian)}")

    def encrypt(self, text):
        """
        Шифрує англійський текст, повертаючи українську шифрограму.

        Args:
            text (str): Англійський текст для шифрування

        Returns:
            str: Українська шифрограма
        """
        if not isinstance(text, str):
            raise ValueError("Вхідний текст має бути рядком")

        result = []
        text = text.lower()  # Переводимо в нижній регістр

        for char in text:
            if char in self.encrypt_map:
                result.append(self.encrypt_map[char])
            else:
                # Невідомі символи залишаємо без змін (цифри, пунктуація)
                result.append(char)

        return ''.join(result)

    def decrypt(self, ciphertext):
        """
        Розшифровує українську шифрограму, повертаючи англійський текст.

        Args:
            ciphertext (str): Українська шифрограма

        Returns:
            str: Розшифрований англійський текст
        """
        if not isinstance(ciphertext, str):
            raise ValueError("Шифрограма має бути рядком")

        result = []

        for char in ciphertext:
            if char in self.decrypt_map:
                result.append(self.decrypt_map[char])
            else:
                # Невідомі символи залишаємо без змін
                result.append(char)

        return ''.join(result)

    def display_mapping(self):
        """Показує повний мапінг літер"""
        print("\nПовний мапінг:")
        print("=" * 60)
        print(f"{'Англійська':>15} | {'Українська':>15} | {'Зворотній мапінг':>20}")
        print("-" * 60)

        for eng_char, ukr_char in sorted(self.encrypt_map.items()):
            eng_display = "пробіл" if eng_char == ' ' else eng_char
            ukr_display = "пробіл" if ukr_char == ' ' else ukr_char
            reverse_check = self.decrypt_map.get(ukr_char, "ПОМИЛКА!")
            reverse_display = "пробіл" if reverse_check == ' ' else reverse_check

            print(f"{eng_display:>15} | {ukr_display:>15} | {reverse_display:>20}")

    def test_reversibility(self):
        """Тестує оборотність шифрування"""
        print("\nТест оборотності:")
        print("="*50)

        test_chars = list(self.encrypt_map.keys())
        all_good = True

        for char in test_chars:
            encrypted = self.encrypt_map[char]
            decrypted = self.decrypt_map.get(encrypted, "ПОМИЛКА")
            is_correct = char == decrypted

            if not is_correct:
                all_good = False

            char_display = "пробіл" if char == ' ' else char
            encrypted_display = "пробіл" if encrypted == ' ' else encrypted
            decrypted_display = "пробіл" if decrypted == ' ' else decrypted

            print(f"{char_display} -> {encrypted_display} -> {decrypted_display} {'✓' if is_correct else '✗'}")

        print(f"\nУсі мапінги оборотні: {'ТАК' if all_good else 'НІ'}")
        return all_good

class TranspositionCipher:
    def __init__(self, word_count=3, word_sizes=[5, 5, 5]):
        """
        Ініціалізує шифр простого пересування.

        Args:
            word_count (int): Кількість слів похідного тексту
            word_sizes (list): Розміри слів похідного тексту
        """
        self.word_count = word_count
        self.word_sizes = word_sizes

        # Генеруємо перестановки для кожного розміру слова
        self.permutations = {}
        for size in set(word_sizes):
            self.permutations[size] = self._generate_all_permutations(size)

        print(f"Ініціалізовано шифр пересування:")
        print(f"Кількість слів: {word_count}")
        print(f"Розміри слів: {word_sizes}")
        print(f"Кількість перестановок для кожного розміру:")
        for size, perms in self.permutations.items():
            print(f"  Розмір {size}: {len(perms)} перестановок")

    def _generate_all_permutations(self, n):
        """
        Генерує всі перестановки n-елементної множини в антилексикографічному порядку.

        Args:
            n (int): Розмір множини

        Returns:
            list: Список всіх перестановок в антилексикографічному порядку
        """
        if n <= 0:
            return [[]]

        # Початкова перестановка (найбільша в антилексикографічному порядку)
        current = list(range(n, 0, -1))  # [n, n-1, ..., 2, 1]
        permutations = [current.copy()]

        while True:
            # Знаходимо наступну перестановку в антилексикографічному порядку
            next_perm = self._next_antilex_permutation(current.copy())
            if next_perm is None:
                break
            permutations.append(next_perm.copy())
            current = next_perm

        return permutations

    def _next_antilex_permutation(self, perm):
        """
        Генерує наступну перестановку в антилексикографічному порядку.

        Args:
            perm (list): Поточна перестановка

        Returns:
            list або None: Наступна перестановка або None, якщо це остання
        """
        n = len(perm)

        # Шукаємо найправіший елемент, який можна зменшити
        i = n - 1
        while i > 0 and perm[i-1] <= perm[i]:
            i -= 1

        if i == 0:
            return None  # Це остання перестановка

        # Знаходимо найбільший елемент справа, який менший за perm[i-1]
        j = n - 1
        while perm[j] >= perm[i-1]:
            j -= 1

        # Обмінюємо елементи
        perm[i-1], perm[j] = perm[j], perm[i-1]

        # Сортуємо суфікс у спадному порядку
        perm[i:] = sorted(perm[i:], reverse=True)

        return perm

    def _apply_permutation(self, text, permutation):
        """
        Застосовує перестановку до тексту.

        Args:
            text (str): Текст для перестановки
            permutation (list): Перестановка (1-індексована)

        Returns:
            str: Переставлений текст
        """
        if len(text) != len(permutation):
            # Якщо текст коротший, доповнюємо пробілами
            text = text.ljust(len(permutation))

        result = [''] * len(permutation)
        for i, pos in enumerate(permutation):
            result[i] = text[pos - 1]  # Перестановка 1-індексована

        return ''.join(result)

    def _reverse_permutation(self, permutation):
        """
        Створює обернену перестановку.

        Args:
            permutation (list): Пряма перестановка

        Returns:
            list: Обернена перестановка
        """
        n = len(permutation)
        reverse = [0] * n
        for i, pos in enumerate(permutation):
            reverse[pos - 1] = i + 1  # 1-індексована
        return reverse

    def encrypt(self, text, permutation_indices=None):
        """
        Шифрує текст за допомогою перестановок.

        Args:
            text (str): Текст для шифрування
            permutation_indices (list): Індекси перестановок для кожного слова
                                      (якщо None, використовуються перші перестановки)

        Returns:
            tuple: (шифрограма, метадані для дешифрування)
        """
        # Зберігаємо оригінальну довжину для правильного дешифрування
        original_length = len(text)

        # Розраховуємо скільки блоків потрібно для всього тексту
        total_predefined_size = sum(self.word_sizes)

        if len(text) > total_predefined_size:
            # Додаємо додаткові блоки для решти тексту
            remaining_text = len(text) - total_predefined_size
            # Використовуємо розмір останнього блоку для додаткових блоків
            last_block_size = self.word_sizes[-1] if self.word_sizes else 5
            additional_blocks_needed = (remaining_text + last_block_size - 1) // last_block_size

            extended_word_sizes = self.word_sizes + [last_block_size] * additional_blocks_needed
            extended_word_count = len(extended_word_sizes)

            print(f"Текст довший за передбачені блоки. Додаємо {additional_blocks_needed} блоків розміру {last_block_size}")
        else:
            extended_word_sizes = self.word_sizes
            extended_word_count = self.word_count

        # Обробляємо індекси перестановок
        if permutation_indices is None:
            permutation_indices = [0] * extended_word_count
        elif len(permutation_indices) < extended_word_count:
            # Розширюємо індекси, повторюючи останній або використовуючи 0
            last_index = permutation_indices[-1] if permutation_indices else 0
            permutation_indices = permutation_indices + [last_index] * (extended_word_count - len(permutation_indices))

        # Розбиваємо текст на блоки відповідно до розширених розмірів слів
        blocks = []
        start = 0

        for i, size in enumerate(extended_word_sizes):
            end = start + size
            if start < len(text):
                block = text[start:end]
                blocks.append(block)
            else:
                blocks.append('')  # Порожній блок, якщо текст закінчився
            start = end

        # Шифруємо кожен блок
        encrypted_blocks = []
        used_permutations = []
        actual_word_sizes = []

        for i, (block, perm_index) in enumerate(zip(blocks, permutation_indices)):
            if not block:  # Пропускаємо порожні блоки
                continue

            word_size = extended_word_sizes[i]
            actual_word_sizes.append(word_size)

            # Переконуємося, що у нас є перестановки для цього розміру
            if word_size not in self.permutations:
                print(f"Генеруємо перестановки для розміру {word_size}")
                self.permutations[word_size] = self._generate_all_permutations(word_size)

            available_perms = self.permutations[word_size]

            if perm_index >= len(available_perms):
                print(f"Попередження: Індекс {perm_index} перевищує кількість перестановок для розміру {word_size}. Використовую індекс 0.")
                perm_index = 0

            permutation = available_perms[perm_index]
            used_permutations.append(permutation.copy())

            encrypted_block = self._apply_permutation(block, permutation)
            encrypted_blocks.append(encrypted_block)

        # Об'єднуємо зашифровані блоки
        ciphertext = ''.join(encrypted_blocks)

        # Метадані для дешифрування
        metadata = {
            'original_length': original_length,
            'word_sizes': actual_word_sizes,
            'permutations': used_permutations,
            'permutation_indices': permutation_indices[:len(actual_word_sizes)]
        }

        return ciphertext, metadata

    def decrypt(self, ciphertext, metadata):
        """
        Дешифрує шифрограму.

        Args:
            ciphertext (str): Шифрограма
            metadata (dict): Метадані з encrypt()

        Returns:
            str: Розшифрований текст
        """
        word_sizes = metadata['word_sizes']
        permutations = metadata['permutations']
        original_length = metadata['original_length']

        # Розбиваємо шифрограму на блоки
        blocks = []
        start = 0

        for size in word_sizes:
            end = start + size
            block = ciphertext[start:end] if start < len(ciphertext) else ''
            blocks.append(block)
            start = end

        # Дешифруємо кожен блок
        decrypted_blocks = []

        for block, permutation in zip(blocks, permutations):
            if not block:
                continue

            # Створюємо обернену перестановку
            reverse_perm = self._reverse_permutation(permutation)

            # Застосовуємо обернену перестановку
            decrypted_block = self._apply_permutation(block, reverse_perm)
            decrypted_blocks.append(decrypted_block)

        # Об'єднуємо блоки та обрізаємо до оригінальної довжини
        result = ''.join(decrypted_blocks)[:original_length]

        return result

    def show_permutations(self, size=5, max_show=10):
        """
        Показує перестановки для заданого розміру.

        Args:
            size (int): Розмір перестановок
            max_show (int): Максимальна кількість перестановок для показу
        """
        if size not in self.permutations:
            print(f"Немає перестановок для розміру {size}")
            return

        perms = self.permutations[size]
        print(f"\nПерестановки для розміру {size} (антилексикографічний порядок):")
        print("=" * 50)

        for i, perm in enumerate(perms[:max_show]):
            print(f"{i:2d}: {perm}")

        if len(perms) > max_show:
            print(f"... та ще {len(perms) - max_show} перестановок")

        print(f"\nЗагальна кількість: {len(perms)} перестановок")

    def demonstrate_encryption(self, text, permutation_indices=None):
        """
        Демонструє процес шифрування з детальним виводом.

        Args:
            text (str): Текст для демонстрації
            permutation_indices (list): Індекси перестановок
        """
        print(f"\nДемонстрація шифрування тексту: '{text}' (довжина: {len(text)})")
        print("=" * 80)

        # Повне шифрування (це також покаже нам розширені блоки)
        ciphertext, metadata = self.encrypt(text, permutation_indices)

        print(f"Використані розміри блоків: {metadata['word_sizes']}")
        print(f"Використані індекси перестановок: {metadata['permutation_indices']}")
        print()

        # Показуємо розбиття на блоки
        start = 0
        for i, (size, permutation, perm_index) in enumerate(zip(
            metadata['word_sizes'],
            metadata['permutations'],
            metadata['permutation_indices']
        )):
            end = start + size
            block = text[start:end] if start < len(text) else ''

            print(f"Блок {i+1} (розмір {size}):")
            print(f"  Позиції в тексті: {start}-{end-1}")
            print(f"  Оригінальний текст: '{block}' (доповнено до '{block.ljust(size)}')")
            print(f"  Перестановка #{perm_index}: {permutation}")

            encrypted_block = self._apply_permutation(block, permutation)
            print(f"  Зашифрований блок: '{encrypted_block}'")
            print()

            start = end

        print(f"Повна шифрограма: '{ciphertext}' (довжина: {len(ciphertext)})")

        # Дешифрування
        decrypted = self.decrypt(ciphertext, metadata)
        print(f"Розшифрований текст: '{decrypted}' (довжина: {len(decrypted)})")
        print(f"Співпадає з оригіналом: {text == decrypted}")


class ColumnarTranspositionCipher:
    def __init__(self, table_size=7):
        """
        Ініціалізує шифр табличного пересування.

        Args:
            table_size (int): Розмір таблиці (кількість стовпців)
        """
        self.table_size = table_size

        # Частоти біграм української мови (включаючи пробіли)
        # Базується на статистичному аналізі українських текстів
        self.ukrainian_bigrams = {
            # Біграми з пробілами (дуже важливі для українського тексту)
            ' н': 0.0180, ' п': 0.0155, ' в': 0.0145, ' з': 0.0135, ' с': 0.0125,
            ' т': 0.0120, ' м': 0.0115, ' д': 0.0110, ' к': 0.0105, ' і': 0.0100,
            'а ': 0.0195, 'е ': 0.0175, 'и ': 0.0165, 'о ': 0.0155, 'і ': 0.0145,
            'у ': 0.0125, 'ь ': 0.0115, 'й ': 0.0105, 'я ': 0.0095, 'ї ': 0.0085,
            # Звичайні біграми (без пробілів)
            'ст': 0.0156, 'ен': 0.0134, 'те': 0.0129, 'на': 0.0126, 'ер': 0.0115,
            'ни': 0.0112, 'ти': 0.0109, 'ор': 0.0107, 'но': 0.0105, 'ро': 0.0102,
            'ал': 0.0098, 'ре': 0.0096, 'ар': 0.0095, 'то': 0.0094, 'ко': 0.0092,
            'ов': 0.0090, 'ел': 0.0089, 'ол': 0.0087, 'ан': 0.0086, 'ра': 0.0085,
            'ос': 0.0084, 'во': 0.0083, 'ле': 0.0082, 'от': 0.0081, 'ні': 0.0080,
            'ло': 0.0079, 'не': 0.0078, 'ес': 0.0077, 'ем': 0.0076, 'ка': 0.0075,
            'ак': 0.0074, 'ир': 0.0073, 'ли': 0.0072, 'ом': 0.0071, 'од': 0.0070,
            'ас': 0.0069, 'ав': 0.0068, 'ед': 0.0067, 'по': 0.0066, 'ил': 0.0065,
            'ад': 0.0064, 'за': 0.0063, 'та': 0.0062, 'ла': 0.0061, 'ри': 0.0060,
            'ет': 0.0059, 'ве': 0.0058, 'ам': 0.0057, 'що': 0.0056, 'да': 0.0055,
            'ма': 0.0054, 'че': 0.0053, 'ва': 0.0052, 'се': 0.0051, 'об': 0.0050,
            'де': 0.0049, 'ме': 0.0048, 'до': 0.0047, 'ки': 0.0046, 'со': 0.0045,
            'па': 0.0044, 'пр': 0.0043, 'ця': 0.0042, 'са': 0.0041, 'го': 0.0040,
            'кт': 0.0039, 'ич': 0.0038, 'ий': 0.0037, 'нн': 0.0036, 'ую': 0.0035,
            'тр': 0.0034, 'сп': 0.0033, 'їх': 0.0032, 'ба': 0.0031, 'бу': 0.0030
        }

        print(f"Ініціалізовано табличний шифр з розміром таблиці: {table_size}")
        print(f"Завантажено {len(self.ukrainian_bigrams)} біграм української мови")

    def encrypt(self, text, key=None):
        """
        Шифрує текст методом табличного пересування.

        Args:
            text (str): Текст для шифрування
            key (list): Ключ - перестановка стовпців (якщо None, використовується [1,3,5,2,7,4,6])

        Returns:
            tuple: (шифрограма, ключ, метадані)
        """
        if key is None:
            # Стандартний ключ для демонстрації
            key = [1, 3, 5, 2, 7, 4, 6]

        if len(key) != self.table_size:
            raise ValueError(f"Ключ має містити {self.table_size} елементів")

        if sorted(key) != list(range(1, self.table_size + 1)):
            raise ValueError(f"Ключ має бути перестановкою чисел від 1 до {self.table_size}")

        # Переводимо в нижній регістр, але зберігаємо пробіли
        clean_text = text.lower()
        original_length = len(clean_text)

        # Доповнюємо текст до повного заповнення таблиці
        rows_needed = (len(clean_text) + self.table_size - 1) // self.table_size
        total_cells = rows_needed * self.table_size
        padded_text = clean_text + 'х' * (total_cells - len(clean_text))

        print(f"Оригінальний текст: '{text}'")
        print(f"Текст у нижньому регістрі: '{clean_text}' (довжина: {len(clean_text)})")
        print(f"Доповнений текст: '{padded_text}' (довжина: {len(padded_text)})")
        print(f"Розмір таблиці: {rows_needed} рядків × {self.table_size} стовпців")
        print(f"Ключ: {key}")

        # Створюємо таблицю
        table = []
        for i in range(rows_needed):
            row = []
            for j in range(self.table_size):
                char_index = i * self.table_size + j
                if char_index < len(padded_text):
                    row.append(padded_text[char_index])
                else:
                    row.append('х')  # Заповнювач
            table.append(row)

        # Показуємо таблицю до перестановки
        print("\nТаблиця до перестановки стовпців:")
        self._print_table(table, list(range(1, self.table_size + 1)))

        # Застосовуємо перестановку стовпців
        permuted_table = []
        for row in table:
            permuted_row = [None] * self.table_size
            for i, col_num in enumerate(key):
                permuted_row[i] = row[col_num - 1]  # key містить номери 1-7, індекси 0-6
            permuted_table.append(permuted_row)

        # Показуємо таблицю після перестановки
        print("\nТаблиця після перестановки стовпців:")
        self._print_table(permuted_table, key)

        # Читаємо по стовпцях для отримання шифрограми
        ciphertext = ""
        for col in range(self.table_size):
            for row in range(rows_needed):
                ciphertext += permuted_table[row][col]

        metadata = {
            'original_length': original_length,
            'rows': rows_needed,
            'padding_chars': total_cells - original_length
        }

        print(f"\nШифрограма: '{ciphertext}'")

        return ciphertext, key, metadata

    def decrypt_with_key(self, ciphertext, key, metadata):
        """
        Розшифровує текст за відомим ключем.

        Args:
            ciphertext (str): Шифрограма
            key (list): Ключ шифрування
            metadata (dict): Метадані з encrypt()

        Returns:
            str: Розшифрований текст
        """
        rows = metadata['rows']

        # Створюємо таблицю з шифрограми (читаємо по стовпцях)
        encrypted_table = []
        for row in range(rows):
            encrypted_table.append([None] * self.table_size)

        char_index = 0
        for col in range(self.table_size):
            for row in range(rows):
                if char_index < len(ciphertext):
                    encrypted_table[row][col] = ciphertext[char_index]
                    char_index += 1

        # Обертаємо перестановку стовпців
        original_table = []
        for row in encrypted_table:
            original_row = [None] * self.table_size
            for i, col_num in enumerate(key):
                original_row[col_num - 1] = row[i]  # Обернена перестановка
            original_table.append(original_row)

        # Читаємо по рядках
        decrypted_text = ""
        for row in original_table:
            for char in row:
                decrypted_text += char

        # Видаляємо доповнення
        original_length = metadata['original_length']
        decrypted_text = decrypted_text[:original_length]

        return decrypted_text

    def _print_table(self, table, column_headers):
        """Виводить таблицю з заголовками стовпців"""
        print("   " + "".join(f"{h:>3}" for h in column_headers))
        print("   " + "-" * (3 * len(column_headers)))
        for i, row in enumerate(table):
            print(f"{i+1:2} " + "".join(f"{cell:>3}" for cell in row))

    def get_bigram_frequencies(self, text):
        """
        Обчислює частоти біграм у тексті.

        Args:
            text (str): Текст для аналізу

        Returns:
            dict: Словник з частотами біграм
        """
        # Переводимо в нижній регістр, але зберігаємо пробіли
        clean_text = text.lower()

        # Рахуємо біграми
        bigrams = []
        for i in range(len(clean_text) - 1):
            bigram = clean_text[i:i+2]
            # Пропускаємо біграми з символом доповнення 'х' на кінці
            if 'х' not in bigram or i < len(clean_text) - 10:  # Ігноруємо 'х' тільки в кінці
                bigrams.append(bigram)

        # Рахуємо частоти
        bigram_count = Counter(bigrams)
        total_bigrams = len(bigrams)

        if total_bigrams == 0:
            return {}

        # Нормалізуємо частоти
        bigram_frequencies = {}
        for bigram, count in bigram_count.items():
            bigram_frequencies[bigram] = count / total_bigrams

        return bigram_frequencies

    def calculate_frequency_error(self, text_frequencies):
        """
        Обчислює похибку частот біграм порівняно з українською мовою.

        Args:
            text_frequencies (dict): Частоти біграм у тексті

        Returns:
            float: Похибка (чи-квадрат статистика)
        """
        error = 0.0

        # Обчислюємо хі-квадрат статистику
        for bigram, expected_freq in self.ukrainian_bigrams.items():
            observed_freq = text_frequencies.get(bigram, 0.0)
            # Використовуємо модифіковану формулу для уникнення ділення на нуль
            if expected_freq > 0:
                error += ((observed_freq - expected_freq) ** 2) / expected_freq

        # Додаємо штраф за біграми, які є у тексті, але не є типовими для української мови
        for bigram, observed_freq in text_frequencies.items():
            if bigram not in self.ukrainian_bigrams and observed_freq > 0.01:  # Штраф за рідкісні біграми
                error += observed_freq * 10  # Штраф

        return error

    def decrypt(self, ciphertext, metadata, max_attempts=1000):
        """
        Розшифровує текст без знання ключа, використовуючи аналіз частот біграм.

        Args:
            ciphertext (str): Шифрограма
            metadata (dict): Метадані з encrypt()
            max_attempts (int): Максимальна кількість перестановок для перевірки

        Returns:
            tuple: (найкращий_текст, найкращий_ключ, похибка, статистики)
        """
        print(f"\nПочинаємо дешифрування без ключа...")
        print(f"Кількість можливих ключів: {math.factorial(self.table_size)} (7! = 5040)")
        print(f"Перевіряємо перші {max_attempts} варіантів")

        best_text = ""
        best_key = None
        best_error = float('inf')
        attempts = 0
        results = []

        # Генеруємо всі можливі перестановки
        for key in itertools.permutations(range(1, self.table_size + 1)):
            if attempts >= max_attempts:
                break

            attempts += 1
            key_list = list(key)

            try:
                # Розшифровуємо з цим ключем
                decrypted_text = self.decrypt_with_key(ciphertext, key_list, metadata)

                # Обчислюємо частоти біграм
                bigram_freq = self.get_bigram_frequencies(decrypted_text)

                # Обчислюємо похибку
                error = self.calculate_frequency_error(bigram_freq)

                # Зберігаємо результат
                results.append({
                    'key': key_list.copy(),
                    'text': decrypted_text,
                    'error': error,
                    'bigram_count': len(bigram_freq)
                })

                # Оновлюємо найкращий результат
                if error < best_error:
                    best_error = error
                    best_text = decrypted_text
                    best_key = key_list.copy()

                # Показуємо прогрес кожні 500 спроб
                if attempts % 500 == 0:
                    print(f"Перевірено {attempts} ключів, найкраща похибка: {best_error:.4f}")

            except Exception as e:
                print(f"Помилка при обробці ключа {key_list}: {e}")
                continue

        # Сортуємо результати за похибкою
        results.sort(key=lambda x: x['error'])

        print(f"\nДешифрування завершено!")
        print(f"Перевірено {attempts} ключів")
        print(f"Найкращий ключ: {best_key}")
        print(f"Найменша похибка: {best_error:.4f}")
        print(f"Розшифрований текст: '{best_text}'")

        # Показуємо топ-5 результатів
        print(f"\nТоп-5 найкращих результатів:")
        print("-" * 80)
        print(f"{'Ранг':<4} {'Ключ':<20} {'Похибка':<12} {'Текст':<30}")
        print("-" * 80)
        for i, result in enumerate(results[:5]):
            key_str = str(result['key'])
            text_preview = result['text'][:25] + "..." if len(result['text']) > 25 else result['text']
            print(f"{i+1:<4} {key_str:<20} {result['error']:<12.4f} {text_preview:<30}")

        statistics = {
            'attempts': attempts,
            'best_error': best_error,
            'top_results': results[:10]  # Топ-10 результатів
        }

        return best_text, best_key, best_error, statistics

    def analyze_bigrams(self, text, show_top=20):
        """
        Аналізує біграми в тексті та порівнює з українською мовою.

        Args:
            text (str): Текст для аналізу
            show_top (int): Кількість топ біграм для показу
        """
        print(f"\nАналіз біграм у тексті: '{text[:50]}{'...' if len(text) > 50 else ''}'")
        print("=" * 80)

        # Отримуємо частоти біграм
        bigram_freq = self.get_bigram_frequencies(text)

        if not bigram_freq:
            print("Текст занадто короткий для аналізу біграм")
            return

        # Сортуємо за частотою
        sorted_bigrams = sorted(bigram_freq.items(), key=lambda x: x[1], reverse=True)

        print(f"Знайдено {len(bigram_freq)} унікальних біграм")
        print(f"\nТоп-{show_top} найчастіших біграм у тексті:")
        print("-" * 60)
        print(f"{'Біграма':<8} {'Частота':<12} {'Еталон УКР':<15} {'Різниця':<10}")
        print("-" * 60)

        for i, (bigram, freq) in enumerate(sorted_bigrams[:show_top]):
            ukrainian_freq = self.ukrainian_bigrams.get(bigram, 0.0)
            difference = freq - ukrainian_freq
            print(f"{bigram:<8} {freq:<12.6f} {ukrainian_freq:<15.6f} {difference:>+9.6f}")

        # Обчислюємо загальну похибку
        error = self.calculate_frequency_error(bigram_freq)
        print(f"\nЗагальна похибка частот: {error:.4f}")

        # Показуємо біграми, які є в українській мові, але відсутні в тексті
        missing_bigrams = []
        for bigram, freq in self.ukrainian_bigrams.items():
            if bigram not in bigram_freq and freq > 0.005:  # Тільки відносно часті біграми
                missing_bigrams.append((bigram, freq))

        if missing_bigrams:
            missing_bigrams.sort(key=lambda x: x[1], reverse=True)
            print(f"\nВідсутні важливі українські біграми (топ-10):")
            print("-" * 40)
            for bigram, freq in missing_bigrams[:10]:
                display_bigram = bigram.replace(' ', '_')
                print(f"{display_bigram:<8} {freq:<12.6f}")


# Демонстрація використання
if __name__ == "__main__":
    # Створюємо шифр
    cipher = ColumnarTranspositionCipher(table_size=7)

    # Тестові тексти
    test_texts = [
        "це тестовий текст для демонстрації роботи шифру табличного пересування",
        "криптографія це наука про методи забезпечення конфіденційності",
        "короткий текст"
    ]

    print("=" * 80)
    print("ДЕМОНСТРАЦІЯ ТАБЛИЧНОГО ШИФРУ")
    print("=" * 80)

    for i, text in enumerate(test_texts):
        print(f"\n{'='*60}")
        print(f"ТЕСТ {i+1}: '{text}'")
        print(f"{'='*60}")

        try:
            # Шифруємо
            ciphertext, key, metadata = cipher.encrypt(text)

            print(f"\n{'-'*40}")
            print("ДЕШИФРУВАННЯ З ВІДОМИМ КЛЮЧЕМ:")
            print(f"{'-'*40}")

            # Дешифруємо з відомим ключем
            decrypted_with_key = cipher.decrypt_with_key(ciphertext, key, metadata)
            print(f"Розшифровано з ключем: '{decrypted_with_key}'")

            # Перевіряємо правильність
            original_clean = text.lower()
            success = original_clean == decrypted_with_key
            print(f"Дешифрування успішне: {success}")

            print(f"\n{'-'*40}")
            print("АНАЛІЗ БІГРАМ ОРИГІНАЛЬНОГО ТЕКСТУ:")
            print(f"{'-'*40}")

            # Аналізуємо біграми оригінального тексту
            cipher.analyze_bigrams(text, show_top=15)

            print(f"\n{'-'*40}")
            print("ДЕШИФРУВАННЯ БЕЗ КЛЮЧА (обмежено 200 спробами):")
            print(f"{'-'*40}")

            # Дешифруємо без ключа (обмежуємо для швидкості)
            best_text, best_key, best_error, stats = cipher.decrypt(
                ciphertext, metadata, max_attempts=200
            )

            # Порівнюємо результати
            print(f"\nПорівняння результатів:")
            print(f"Оригінальний ключ:    {key}")
            print(f"Знайдений ключ:       {best_key}")
            print(f"Ключі співпадають:    {key == best_key}")
            print(f"Оригінальний текст:   '{original_clean}'")
            print(f"Знайдений текст:      '{best_text}'")
            print(f"Тексти співпадають:   {original_clean == best_text}")

        except Exception as e:
            print(f"Помилка: {e}")
            import traceback
            traceback.print_exc()

    # Демонстрація аналізу похибок
    print(f"\n{'='*80}")
    print("ДЕМОНСТРАЦІЯ АНАЛІЗУ ПОХИБОК ЧАСТОТ")
    print(f"{'='*80}")

    sample_texts = [
        "це типовий український текст з біграмами",
        "this is english text with different bigrams",
        "абракадабра невідомий текст зі штучними біграмами"
    ]

    for text in sample_texts:
        print(f"\n{'-'*50}")
        cipher.analyze_bigrams(text, show_top=10)
