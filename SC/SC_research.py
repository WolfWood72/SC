from Scrembler import Scrembler




poly = [0,3,9]
N = 100
for i in [51,100, 653, 963]:
    print("LEN = {}".format(i))
    SC = Scrembler(init_value=i ,polynom=poly)
    key = SC.GetSequence(N)
