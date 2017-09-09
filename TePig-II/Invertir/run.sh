cd /root/Bolsa/TePig-II/Invertir

python invertir.py OHL > correo.txt
python invertir.py GSJ >> correo.txt
python invertir.py ECR >> correo.txt
python invertir.py EZE >> correo.txt
python invertir.py ADZ >> correo.txt
python invertir.py SLR >> correo.txt
python invertir.py AZK >> correo.txt

python enviarCorreo.py

 
