cd /root/Bolsa/PajaroLoco/Invertir
echo "Ind,Ops,Dinero,Rent,Benef,OutBB,MeanDinOps" > correo_todo.txt
python invertir.py ACX >> correo_todo.txt
python invertir.py ACS >> correo_todo.txt
python invertir.py APAM >> correo_todo.txt
python invertir.py A3M >> correo_todo.txt
python invertir.py SAB >> correo_todo.txt
python invertir.py SAN >> correo_todo.txt
python invertir.py BAIN >> correo_todo.txt
python invertir.py FCC >> correo_todo.txt
python invertir.py GCO >> correo_todo.txt
python invertir.py IAG >> correo_todo.txt
python invertir.py TL5 >> correo_todo.txt
python invertir.py TEF >> correo_todo.txt
python invertir.py CAF >> correo_todo.txt
python invertir.py TLGO >> correo_todo.txt
python invertir.py TUB >> correo_todo.txt
python invertir.py ENC >> correo_todo.txt

echo "##########################################################################################################################" > correo.txt
cat correo_todo.txt | grep INVERTIR >> correo.txt
echo "##########################################################################################################################" >> correo.txt
cat correo_todo.txt >> correo.txt
echo "##########################################################################################################################" >> correo.txt

python enviarCorreo.py




