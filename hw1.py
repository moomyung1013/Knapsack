class Bob:
    def __init__(self, b, n, r):
        self.b = b
        self.n = n
        self.r = r
        _, self.rd, _ = self.egcd(self.r, self.n)

    def keyGenerate(self):
        t = [b_ * self.r % self.n for b_ in self.b]
        a = self.knapsackPermute(t)     # public
        print("Bob generates keys\nt:", t, "\na:", a)
        print("Bob's private (n, r, rd, b): ", self.n, self.r, self.rd, self.b, "\n")
        return a

    def knapsackPermute(self, per):
        p = [4, 2, 5, 3, 1, 7, 6]  # 치환표
        data = [0 for _ in range(len(per))]
        for idx, val in enumerate(p):
            data[idx] = per[val - 1]
        return data

    def inv_knapsackSum(self, s_):
        t = [0 for _ in range(len(self.b))]
        new_b = reversed(self.b)
        for idx, val in enumerate(new_b):
            if s_ >= val:
                t[len(self.b) - 1 - idx] = 1
                s_ -= val
        return t

    def egcd(self, a, b):
        if a == 0:
            return b, 0, 1
        else:
            g, y, x = self.egcd(b % a, a)
            return g, x - (b // a) * y, y

    def decode(self, s):
        s_ = self.rd * s % self.n
        x_ = self.inv_knapsackSum(s_)
        x = self.knapsackPermute(x_)
        plain = "".join([str(_) for _ in x])
        decode_ch = chr(int(plain, 2))
        print("Bob computes:\ns\':", s_, "\nx\':", x_, "\nx:", x)
        print("Bob이 복호화한 암호문:", decode_ch)


class Alice:
    def __init__(self, ch, a):
        self.ch = ch
        self.a = a
        self.x = []

    def makePlainText(self):
        self.x = list(map(int, format(ord(self.ch), 'b')))  # 평문

    def makeCipherText(self):
        s = self.knapsackSum()
        print("Alice data:", self.x)
        print("Alice make cypertext:", s, "and sends it.\n")
        return s  # 암호문

    def knapsackSum(self):
        sum_data = 0
        for idx, val in enumerate(self.a):
            sum_data += (val * self.x[idx])
        return sum_data


Bob_n, Bob_r, Bob_b = 900, 37, [7, 11, 19, 39, 79, 157, 313]
bob = Bob(Bob_b, Bob_n, Bob_r)
public_a = bob.keyGenerate()

Alice_ch = 'g'
alice = Alice(Alice_ch, public_a)
alice.makePlainText()
s = alice.makeCipherText()

bob.decode(s)
