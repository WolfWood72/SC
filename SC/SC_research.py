from Scrembler import Scrembler




poly1 = [0,3,9]
N = 200
for i in [79, 124, 623]:
    print("init = {}".format(i))
    SC = Scrembler(init_value=i ,polynom=poly1)
    key = SC.GetSequence(N)


poly2 = [0, 4, 9]
for i in [79, 124, 623]:
    print("init = {}".format(i))
    SC = Scrembler(init_value=i ,polynom=poly2)
    key = SC.GetSequence(N)