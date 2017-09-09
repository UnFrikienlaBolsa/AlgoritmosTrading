cd /root/Bolsa/Medias/Invertir
python test.py SAB > correo.txt
python test.py COL >> correo.txt
python test.py ECR >> correo.txt
python test.py IAG >> correo.txt
python test.py NEA >> correo.txt
python test.py APAM >> correo.txt
python test.py MRL >> correo.txt
python test.py ACX >> correo.txt
python test.py AENA >> correo.txt
python test.py BKT >> correo.txt
python test.py APAM >> correo.txt
python test.py TUB >> correo.txt

python enviarCorreo.py

