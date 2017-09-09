#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 27 12:01:22 2017

Envia por correo electronico los resultados obtenidos

"""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time
 
# UTILIDADES
def SendMail(tituloCorreo, html):
    toaddrs  = ['rubenglezant@gmail.com']
    
    # Record the MIME types of both parts - text/plain and text/html.
    part1 = MIMEText("", 'plain')
    part2 = MIMEText(html, 'html')
    
    fromaddr = 'pcillo2mar@gmail.com'
    
    for destino in toaddrs:
    	msg = MIMEMultipart('alternative')
    	msg['Subject'] = tituloCorreo + ' - ' + time.strftime("%c")
    	msg['From'] = fromaddr
    	msg['To'] = " "
    	msg.attach(part1)
    	msg.attach(part2)
    	username = 'pcillo2mar@gmail.com'
    	password = 'XXXXXXXXXX'
    	server = smtplib.SMTP('smtp.gmail.com:587')
    	server.ehlo()
    	server.starttls()
    	server.login(username,password)
    	#server.sendmail(me, you, msg.as_string())
    	server.sendmail(fromaddr, destino, msg.as_string())
    	server.quit()

html = ""
titulo = "KO - SOLO INFO - Alg. MEDIAS"
with open("correo.txt", "r") as ins:
    for line in ins:
        html = html + line + "<br />"
        if ('INVERTIR' in line):
            titulo = 'INVERTIR! Alg. MEDIAS'

SendMail(titulo,html)
