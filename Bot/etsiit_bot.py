# --* coding: utf-8 -*-

import telebot 
from telebot import types 
import urllib2, cookielib, os.path, time, sys

sys.path.append('../informacion/')
from conf import token


reload(sys) 
sys.setdefaultencoding("utf-8")

bot = telebot.TeleBot(token) # Creamos el objeto de nuestro bot.

def listener(messages):
    for m in messages: 
        user_id = m.from_user.id
        
bot.set_update_listener(listener) 

# Funcion start

@bot.message_handler(commands=['start'])
def start(m):
    
    log(m)
    
    cid = m.chat.id

    mensaje = "¡Hola!\n\nSoy el bot no oficial de la E.T.S.I.I.T de Granada" \
    ", estoy aqui para proporcionarte informacion sobre ella, como horarios, examenes..\n" \
    "Actualmente estoy en construccion, si echas en falta alguna funcionalidad puedes " \
    "enviarnos una sugerencia o, ¡incorporarla tu mismo!\n\n" \
    "Contacto: acasadoquijada@gmail.com\n" \
    "Repositorio: https://github.com/acasadoquijada/ETSIIT_BOT\n"
    bot.send_message(cid,mensaje)
    
#Ayuda

@bot.message_handler(commands=['ayuda'])
def ayuda(m):
    
    log(m)
    
    cid = m.chat.id
    
    mensaje = "¡Hola!\n\nEstas son las funciones de las que dispongo:\n\n"\
    "/horario_gii - Horario 2015/2016 para ingeniería informática.\n" \
    "/horario_git - Horario 2015/2016 para ingeniería en telecomunicaciones.\n"\
    "/horario_gim - Horario 2015/2016 para doble grado informática matemáticas.\n"\
    "/examenes - Examenes del curso 2015/2016 para todos los grados.\n"\
    "/examenes_gii - Exámenes grado ingeniería informática del curso 2015/2016.\n"\
    "/examenes_gitt - Exámenes grado ingeniería telecomunicaciones del curso 2015/2016.\n"\
    "/localizacion - Localizacion de la escuela en google maps.\n"\
    "/contacto - Información de contacto de los desarrolladores.\n\n"\
    "Contacto: acasadoquijada@gmail.com\n" \
    "Repositorio: https://github.com/acasadoquijada/ETSIIT_BOT\n"
    
    bot.send_message(cid,mensaje)


#Registro de actividad
def log(m):
    user_id = m.from_user.id
    name = m.from_user.first_name
    last_name = m.from_user.last_name
    username = m.from_user.username
    hour = time.strftime("%H:%M:%S")
    date = time.strftime("%d/%m/%y")
    information = "["+ str(date) + ' ' + str(hour) + ' ' +str(name)  + ' ' +  str(last_name) + ' ' + str(user_id) + ' @' + str(username) + "]: " + m.text 
    
    aux = open( '../informacion/registro.txt', 'a')
    aux.write( str(information) + "\n")
    aux.close()
 
def exception_log(e,m):
    hour = time.strftime("%H:%M:%S")
    date = time.strftime("%d/%m/%y")
        
    complete_date = 'Times exception: '  + str(date) + ' ' + str(hour) + '\n'
    
    cause = 'Cause of the exception: ' + str(m.text) + '\n'
    
    exception = 'Exception: ' + str(e)
    
    information = complete_date + cause + exception
    
    
    aux = open( '../informacion/exception.txt', 'a') 
    aux.write( str(information) + "\n\n")
    aux.close()       
    
    
bot.polling(none_stop=True) 


# Comprobamos si existe el horario y se actua en consecuencia
def mandar_horario(grado,m):
    
    try:
        log(m)
        path = '../Horarios/'
        nombre_fichero = 'horarios_gi'
        descriptor = 'horariosgi'
        
        if grado == 'informatica':
            descriptor += 'i1516/!'
            nombre_fichero += 'i.pdf'
            
        elif grado == 'teleco':
            descriptor += 'tt1516/!'
            nombre_fichero += 't.pdf'
        
        elif grado == 'matematicas':
           descriptor +=  'm1516/!'
           nombre_fichero += 'm.pdf'
        
        if os.path.isfile(path + nombre_fichero):
            bot.send_chat_action(m.chat.id,'upload_document')

            bot.send_document(m.chat.id, open( path + nombre_fichero, 'rb'))
        
        else:
            url = 'http://etsiit.ugr.es/pages/calendario_academico/horarios1516/' + descriptor
            cj = cookielib.CookieJar()
        
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            
            request = urllib2.Request(url)
            
            f = opener.open(request)
            data = f.read()
            f.close()
            opener.close()
            
            FILE = open(path + nombre_fichero, "wb+")
            FILE.write(data)
            FILE.close()

            bot.send_chat_action(m.chat.id,'upload_document')
            
            bot.send_document(m.chat.id, open( path + nombre_fichero, 'rb'))
            
    except Exception as e:
        bot.reply_to(m,'Se ha producido un error, intentelo mas tarde')
        exception_log(e,m)


# Comprobamos si existe el horario y se actua en consecuencia
def mandar_examenes(grado,m):
    
    try:
        log(m)
        path = '../examenes/'
        nombre_fichero = ''

        
        if grado == 'informatica':
            nombre_fichero += 'examenes_gii.pdf'

        elif grado == 'teleco':
            nombre_fichero += 'examenes_gitt.pdf'


        if os.path.isfile(path + nombre_fichero):
            bot.send_chat_action(m.chat.id,'upload_document')

            bot.send_document(m.chat.id, open( path + nombre_fichero, 'rb'))
        
        else:
            bot.reply_to(m,'Se ha producido un error, intentelo mas tarde')

            
    except Exception as e:
        bot.reply_to(m,'Se ha producido un error, intentelo mas tarde')
        exception_log(e,m)

# Contacto

@bot.message_handler(commands=['contacto'])
def contacto(m):
    
    log(m)
    
    cid = m.chat.id

    mensaje = "Información de contacto de la escuela:\n\n" \
    "Teléfono: +34 958242802\n" \
    "Fax: +34 958242801\n" \

    bot.send_message(cid,mensaje)    
    




#Examenes grado ingenieria informatica
    
@bot.message_handler(commands=['examenes_gii'])
def obtener_examenes_gii(m):
    mandar_examenes('informatica',m)
    
#Examenes grado ingenieria informatica
    
@bot.message_handler(commands=['examenes_gitt'])
def obtener_examenes_gitt(m):
    mandar_examenes('teleco',m)
    
    
#Horario grado ingenieria informatica
    
@bot.message_handler(commands=['horario_gii'])
def obtener_horario_gii(m):
    mandar_horario('informatica',m)


#Horario grado ingenieria telecomunicaciones

@bot.message_handler(commands=['horario_git'])
def obtener_horario_git(m):
    mandar_horario('teleco',m)
        
#Horario grado ingenieria inf+mates

@bot.message_handler(commands=['horario_gim'])
def obtener_horario_gim(m):
    mandar_horario('matematicas',m)

# Examenes    
@bot.message_handler(commands=['examenes'])
def obtener_examenes(m):
    try:
        if os.path.isfile('../examenes/examenes.pdf'):
            bot.send_chat_action(m.chat.id,'upload_document')

            bot.send_document(m.chat.id, open( '../examenes/examenes.pdf', 'rb'))
        
        else:
            url = 'http://etsiit.ugr.es/pages/calendario_academico/calendarioexamenes1516/!'
            cj = cookielib.CookieJar()
        
            opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
            
            request = urllib2.Request(url)
            
            f = opener.open(request)
            data = f.read()
            f.close()
            opener.close()
            
            FILE = open('../examenes/examenes.pdf', "wb+")
            FILE.write(data)
            FILE.close()
            
            bot.send_document(m.chat.id, open( '../examenes/examenes.pdf', 'rb'))
            
    except Exception as e:
        bot.reply_to(m,'Se ha producido un error, intentelo mas tarde')
        exception_log(e,m)


# Envia localizacion
@bot.message_handler(commands=['localizacion'])
def obtener_localizacion(m):

    try:
        log(m)

        cid = m.chat.id
        
        bot.send_location(cid,37.196689,-3.624534)
    except Exception as e:
        bot.reply_to(m,'Se ha producido un error, intentelo mas tarde')
        exception_log(e,m)
        
# Envia web
@bot.message_handler(commands=['web'])
def obtener_web(m):

    try:
        log(m)

        cid = m.chat.id
        mensaje = 'Aquí tienes la web de la ETSIIT: '
        
        bot.send_message(cid,mensaje + 'http://etsiit.ugr.es/')
    except Exception as e:
        bot.reply_to(m,'Se ha producido un error, intentelo mas tarde')
        exception_log(e,m)
        


while True: 
    time.sleep(300)