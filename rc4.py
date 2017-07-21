class RC4:
    def __init__(self, password, drop = 0):
        self.s = [] * 256
        self._ksa(password)
        self.i = 0
        self.j = 0
        for d in range(drop):
            self.next_byte()

    def _swap(self, index1, index2):
        t = self.s[index1]
        self.s[index1] = self.s[index2]
        self.s[index2] = t

    def next_byte(self):
        self.i = (self.i + 1) % 256
        self.j = (self.j + self.s[self.i]) % 256
        self._swap(self.i, self.j)
        return self.s[(self.s[self.i] + self.s[self.j]) % 256]

    def _ksa(self, password):
        for i in range(256):
            self.s[i] = i
        j = 0
        for i in range(256):
            j = (j + self.s[i] + ord(password[i % len(password)])) % 256
            self._swap(i, j)

