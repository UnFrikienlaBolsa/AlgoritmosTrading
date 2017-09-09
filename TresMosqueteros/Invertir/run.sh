cd /root/Bolsa/TresMosqueteros/Invertir

python linearRegresionInvertir2.py A3M > correo.txt
python linearRegresionInvertir2.py ADZ >> correo.txt
python linearRegresionInvertir2.py CBAV >> correo.txt
python linearRegresionInvertir2.py BIO >> correo.txt
python linearRegresionInvertir2.py MDF >> correo.txt
python linearRegresionInvertir2.py LBK >> correo.txt
python linearRegresionInvertir2.py OHL >> correo.txt
python linearRegresionInvertir2.py TL5 >> correo.txt

python enviarCorreo.py



