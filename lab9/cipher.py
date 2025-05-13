class RSA_sign:
    def __init__(self, n, e, d=None):
        """
        Ініціалізація RSA підпису
        n - модуль (p*q)
        e - відкритий показник степеня
        d - секретний показник степеня (опціонально, потрібен для створення підпису)
        """
        self.n = n
        self.e = e
        self.d = d

    def sign(self, m):
        """
        Створення цифрового підпису для хеш-значення m
        m - хеш-значення повідомлення
        Повертає підпис s = m^d mod n
        """
        if self.d is None:
            raise ValueError("Секретний ключ (d) необхідний для створення підпису")
        return pow(m, self.d, self.n)

    def verify(self, m, s):
        """
        Перевірка підпису
        m - хеш-значення повідомлення
        s - цифровий підпис
        Повертає True, якщо підпис дійсний
        """
        # Перевірка підпису: m =?= s^e mod n
        return m == pow(s, self.e, self.n)

class ElGamal_sign:
    def __init__(self, p, g, x=None, y=None):
        """
        Ініціалізація підпису Ель-Гамаля
        p - велике просте число
        g - первісний корінь p
        x - секретний ключ (опціонально)
        y - відкритий ключ (якщо не надано, обчислюється як g^x mod p)
        """
        self.p = p
        self.g = g
        self.x = x  # Секретний ключ

        if y is None and x is not None:
            self.y = pow(g, x, p)  # Обчислюємо відкритий ключ
        else:
            self.y = y

    def extended_gcd(self, a, b):
        """Розширений алгоритм Евкліда для знаходження НСД(a, b) та коефіцієнтів Безу"""
        if a == 0:
            return b, 0, 1
        else:
            gcd, x, y = self.extended_gcd(b % a, a)
            return gcd, y - (b // a) * x, x

    def mod_inverse(self, k, p):
        """Знаходження мультиплікативного оберненого за модулем p"""
        gcd, x, y = self.extended_gcd(k, p)
        if gcd != 1:
            raise Exception('Мультиплікативний обернений не існує')
        else:
            return x % p

    def sign(self, m, k=None):
        """
        Створення підпису для хеш-значення m
        m - хеш-значення повідомлення
        k - секретне випадкове число (опціонально)
        Повертає пару (a, b) - цифровий підпис
        """
        if self.x is None:
            raise ValueError("Секретний ключ (x) необхідний для створення підпису")

        if k is None:
            import random
            # Вибираємо випадкове k, взаємно просте з p-1
            k = random.randint(2, self.p-2)
            while self.extended_gcd(k, self.p-1)[0] != 1:
                k = random.randint(2, self.p-2)
        else:
            if self.extended_gcd(k, self.p-1)[0] != 1:
                raise ValueError("k має бути взаємно простим з (p-1)")

        # Обчислюємо a = g^k mod p
        a = pow(self.g, k, self.p)

        # Обчислюємо k^-1 mod (p-1)
        k_inv = self.mod_inverse(k, self.p-1)

        # Обчислюємо b = k^-1 * (m - x * a) mod (p-1)
        b = (k_inv * (m - self.x * a)) % (self.p-1)

        return a, b

    def verify(self, m, signature):
        """
        Перевірка підпису
        m - хеш-значення повідомлення
        signature - пара (a, b) - цифровий підпис
        Повертає True, якщо підпис дійсний
        """
        a, b = signature

        # Перевірка: y^a * a^b mod p =?= g^m mod p
        left = (pow(self.y, a, self.p) * pow(a, b, self.p)) % self.p
        right = pow(self.g, m, self.p)

        return left == right
