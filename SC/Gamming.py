        
class Gamming:
    def __init__(self, key, key_format="BIN"):
        self.key = key
        if key_format == "BIN":
            self.key = self.FromBin(key)
        elif key_format == "HEX":
            self.key = self.FromHex(key)
        elif key_format == "SYM":
            self.key = self.FromSym(key)
        elif key_format == "ARR":
            self.key = key



    def FormatStringToByteArr(self, str, str_format):
        res = None
        if str_format == "BIN":
            res = self.FromBin(str)
        elif str_format == "HEX":
            res = self.FromHex(str)
        elif str_format == "SYM":
            res = self.FromSym(str)
        else:
            res = str
        return res 


    def IntToBitArray(self,n):
        return [int(digit) for digit in bin(n)[2:]]

    def FromBin(self, val):
        arr = []
        for i in val:
            arr.append(int(i))
        return arr

    def FromHex(self, val):
        arr = [] 
        for i in val.split(" "):
            arr+= self.IntToBitArray((i, 16))

    def FromSym(self, s):
        result = []
        for c in s:
            bits = bin(ord(c))[2:]
            bits = '00000000'[len(bits):] + bits
            result.extend([int(b) for b in bits])
        return result
        #arr = []
        #for i in val:
        #    arr+= self.IntToBitArray( ord(i))
        #return arr

    def GetStringBin(self, arr):
        return ''.join(str(e) for e in arr)

    def GetStringHex(self, val):
        n = int(len(val)/7)
        res = ""
        for i in range(n):
            t = "".join( str(e) for e in val[i*7 : (i+1)*7])+" "
            res+= hex(int(t,2)).split('x')[-1]
        return res

    def GetStringSym(self, bits):
       #n = int(len(val)/7)#
       #res = ""
       #for i in range(n):
       #    t = "".join( str(e) for e in val[i*7 : (i+1)*7])+" "
       #    res+= chr(int(t,2))
       #return res
      # while len(bits)%8 !=0:
     #      bits = [0] + bits#
       chars = []
       for b in range(int(len(bits) / 8)):
           byte = bits[b * 8:(b + 1) * 8]
           chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))
       return ''.join(chars)


    def ByteArrToFormatString(self, arr, format):
        res = None
        if format == "BIN":
            res = self.GetStringBin(arr)
        elif format == "HEX":
            res = self.GetStringHex(arr)
        elif format == "SYM":
            res = self.GetStringSym(arr)
        else:
            res = arr
        return res



    def set_key(self, key):
        self.key = key

    def get_key(self):
        return self.key
    
    def encode(self,messege, messege_format):
        mes = self.FormatStringToByteArr(messege, messege_format)
        code = [ m[0]^m[1] for m in zip(self.key,mes) ]
        return code
        
    def decode(self, code, code_format):
        code = self.FormatStringToByteArr(code, code_format)
        mes = [ m[0]^m[1] for m in zip(self.key,code) ]
        return mes
    


