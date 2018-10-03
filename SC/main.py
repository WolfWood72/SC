from Scrembler import Scrembler
from  Gamming import Gamming
import argparse
import sys

parser = argparse.ArgumentParser()
parser.add_argument("-encode", "-encode", action='store_true',
                    help="input file", required=False)
parser.add_argument("-decode","-decode",  action='store_true',
                    help="input file", required=False)
parser.add_argument("-input_file", type=str,
                    help="file with input message", nargs="*")
parser.add_argument("-output_file", type=str,
                    help="file with output message", nargs="*")
parser.add_argument("-init_val_file", type=str,
                    help="file with init value for scrembler", nargs="*")
namespace = parser.parse_args(sys.argv[1:])

input_file = None
input_format = None

output_file = None
output_format = None

init_value_file =None
init_value_format = None

try:
    if not namespace.decode and not namespace.encode:
        raise ValueError("must have decode or encode param")
    if namespace.decode and namespace.encode:
        raise ValueError("must have only one of encode and deocde param")

    input_file,input_format = namespace.input_file [0], namespace.input_file[1]
    output_file, output_format = namespace.output_file[0], namespace.output_file[1]
    init_value_file, init_value_format = namespace.init_val_file[0], namespace.init_val_file[1]

except Exception as e:
    print(str(e))
    exit("err")

input_mess = None
with open(input_file, "r",encoding = "utf-8") as f:
    input_mess = f.read()

init_value = None
with open(init_value_file, "r") as f:
    init_value_mess = int(f.read())

poly = [0,3,9, 15 ,16 , 20]

SC = Scrembler(init_value=init_value_mess ,polynom=poly)


N = len(input_mess) if input_format == "BIN" else len(input_mess)*8

key = SC.GetSequence(N)

G = Gamming(key)
print("Введнное сообщение: " + input_mess)
#print(G.FromSym(input_mess))
if namespace.encode:
   encoded_mes =  G.encode(input_mess, input_format)
   print(encoded_mes)
   ba = G.ByteArrToFormatString(encoded_mes, output_format)
   print("Зашифрованное сообщение: " + ba)


   decoded_mes = G.decode(ba, "SYM")
   print(decoded_mes)
   print(G.ByteArrToFormatString(decoded_mes,output_format))



   with open(output_file, "w",encoding = "utf-8") as f:
       f.write(G.ByteArrToFormatString(encoded_mes, output_format))

elif namespace.decode:
    decoded_mes = G.decode(input_mess, input_format)
    print(decoded_mes)
    print("Расшифрованное сообщение:" + G.ByteArrToFormatString(decoded_mes, output_format))
    with open(output_file, "w",encoding = "utf-8") as f:
        f.write(G.ByteArrToFormatString(decoded_mes, output_format))


