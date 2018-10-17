from scipy.stats import chisquare
import os

fileDir = os.path.dirname(__file__)


class Scrambler:

    def __init__(self):

        self.sp_seq = []
        #self.polynom = {1: [8, 7, 6, 3, 2, 0], 2: [8, 5, 3, 2, 0]}
        self.polynom = {1: [ 7,6,2 ], 2: [9,4, 0]}
        self.dim = {1: 8, 2: 8}
        self.ref_gam = None
        self.poly_num = None


    def make_format(self, value,  n_bit):
        _format = '0' + str(n_bit) + 'b'
        if value.isdecimal():
            return [int(j) for j in format(int(value), _format)]
        else:
            return [int(j) for j in ''.join(format(ord(i), '08b') for i in value)]

    def is_balanced(self, interval_len):
        zeros = self.sp_seq[:interval_len].count(0)
        units = interval_len - zeros
        n = len(self.sp_seq)
        for i in range(interval_len, n):
            if abs(zeros - units) / interval_len > 0.05:
                return False

            if self.sp_seq[i] == 1:
                units += 1
            else:
                zeros += 1

            if self.sp_seq[i - interval_len] == 1:
                units -= 1
            else:
                zeros -= 1
        return True

    def is_cycled(self):

        n = len(self.sp_seq)

        max_cycle_len = n // 2

        for cycle_len in reversed(range(2, max_cycle_len + 1)):
            interval_num = n // cycle_len
            interval_example = self.sp_seq[:cycle_len]
            cycled = True
            for i in range(interval_num):
                cur_interval = self.sp_seq[i * cycle_len: (i + 1) * cycle_len]
                m = len(cur_interval)
                if cur_interval != interval_example[:m]:
                    cycled = False
                    break

            if cycled:
                return cycle_len

        return 0

    def correlation(self, shift):
        shifted_seq = self.sp_seq[-shift:] + self.sp_seq[:-shift]
        equal = 0
        for i in range(len(self.sp_seq)):
            if self.sp_seq[i] == shifted_seq[i]:
                equal += 1
        if (equal / len(self.sp_seq)) > 0.95:
            return True
        else:
            return False

    def coding(self):

        with open(os.path.join(fileDir, "for_coding.txt"), 'r', encoding='utf-8') as file:
            input_text = file.read().upper()

        text = list(self.make_format(input_text, self.dim[self.poly_num]))

        coded = []
        gam = list(self.ref_gam)

        for char in text:
            self.sp_seq.append(gam[-1])
            scramb_b = 0
            for i in self.polynom[self.poly_num]:
                scramb_b ^= gam[self.dim[self.poly_num] - 1 - i]
            char ^= scramb_b
            coded.append(char)
            gam = [char] + gam[:-1]

        b = self.dim[self.poly_num]
        n = len(coded) // b
        with open(os.path.join(fileDir, "for_decoding.txt"), 'w', encoding='utf-8') as file:
            for i in range(n):
                tmp = ''.join(str(j) for j in coded[i * b: i * b + b])
                file.write(chr(int(tmp, 2)))

        with open(os.path.join(fileDir, "gam.txt"), 'w', encoding='utf-8') as file:
            for i in self.sp_seq:
                file.write(str(i))

        print('Последовательность сохранена в файл gam.txt\n')

    def decoding(self):
        with open(os.path.join(fileDir, "for_decoding.txt"), 'r', encoding='utf-8') as file:
            input_text = file.read().upper()

        text = list(self.make_format(input_text, self.dim[self.poly_num]))

        gam = list(self.ref_gam)
        decode = []

        for char in text:
            scramb_b = 0
            for i in self.polynom[self.poly_num]:
                scramb_b ^= gam[self.dim[self.poly_num] - 1 - i]
            scramb_b ^= char
            decode.append(scramb_b)
            gam = [char] + gam[:-1]

        b = self.dim[self.poly_num]
        n = len(decode) // b
        with open(os.path.join(fileDir, "output.txt"), 'w', encoding='utf-8') as file:
            for i in range(n):
                tmp = ''.join(str(j) for j in decode[i * b: i * b + b])
                file.write(chr(int(tmp, 2)))

    def do(self):

        print('Выберете скремблер:\n1 - x^8 + x^7 + x^6 + x^3 + x^2 + 1\n2 - x^8 + x^5 + x^3 + x^2 + 1')
        self.poly_num = int(input())
        print('Введите ключ: ')
        key = input()

        self.ref_gam = list(self.make_format(key, self.dim[self.poly_num]))

        self.coding()

        self.decoding()

        sb = True
        for i in range(1, len(self.sp_seq)):
            if self.is_balanced(i):
                sb = False
                print('Сбалансированность при длинне интервала ' + str(i))
                break
        if sb:
            print('Последовательность не сбалансированна')

        if self.is_cycled() == 0:
            print("Цикличность отсутствует")
        else:
            print("Цикличность присутствует")

        if self.correlation(10) is False:
            print("Корреляция отсутствует")
        else:
            print("Корреляция присутствует")

        z = self.sp_seq.count(0) / len(self.sp_seq)
        o = self.sp_seq.count(1) / len(self.sp_seq)
        print(chisquare([z, o]))


sc = Scrambler()

sc.do() 


#gam = [int(j) for j in gam]
#_gam = list(gam)

#print(gam)

#text = 'Base, base, it’s cheeseburger 1. Can you hear me?'
#text = [int(j) for j in ''.join(format(ord(i), '08b') for i in text)]
#code = []

#sp = []

#P = 0

#for char in text:
#    sp.append(_gam[-1])
#    scramb_b = 0
#    for i in poly:
#        scramb_b ^= _gam[r - 1 - i]
#    char ^= scramb_b
#    code.append(char)
#    _gam = [char] + _gam[:-1]
#    if _gam != gam:
#        P += 1

#print(sp)

#print(text, code)
#print(P)


#for i in range(1, len(text)):
#    if is_balanced(sp, i):
#        print(i)
#        break

#print(is_cycled(sp))

#print(correlation(sp, 1))

#z = sp.count(0) / len(sp)
#o = sp.count(1) / len(sp)

#print(chisquare([z, o]))

#decode = []
#print(gam)

#output = 0
#for char in code:
#    scramb_b = 0
#    for i in poly:
#        scramb_b ^= gam[r - 1 - i]
#    scramb_b ^= char
#    decode.append(scramb_b)
#    gam = [char] + gam[:-1]
#    print(gam)

#print(text, decode)

