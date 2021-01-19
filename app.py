from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL
import logging
import wikipedia



global bot
global TOKEN
TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)


#Empezamos la app de flask
app = Flask(__name__)



@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():
   # Retornamos el mensaje y despues lo pasamos a un objeto de telegram
   update = telegram.Update.de_json(request.get_json(force=True), bot)

   chat_id = update.message.chat.id
   msg_id = update.message.message_id

   # Telegram entiende utf-8
   text = update.message.text.encode('utf-8').decode()
   wikipedia.set_lang("es")
   # El mensaje de bienvenida
   if text == "/start":
       # Mostramos el mensaje de bienvenida
       bot_welcome = """
       Bienvenido al WikiBot, este bot fue creado por Danilo Diez y esta pensado para gente curiosa. Lo unico que tenes que hacer es enviar un mensaje con el tema que te interesa y vas a recibir un extracto de la Wikipedia para que respondas tu curiosidad.
       Para configurar el idioma enviar un mensaje con /en o /es
       """
       # Enviamos el mensaje de bienvenida
       bot.sendMessage(chat_id=chat_id, text=bot_welcome, reply_to_message_id=msg_id)

    
    else if(text == "/en"):
        wikipedia.set_lang("en")
    else if(text == "/es"):
        wikipedia.set_lang("es")
   else:
       try:
           # Parseamos la consulta para no tener espacios
           query = text.strip()
           query = " ".join(text.split())
           
           
           #Hacemos la peticion

           wiki = wikipedia.page(query).content
           url_wiki = wikipedia.page(query).url
           
           #Truncamos el contenido para que quepa en un mensaje
           wiki = wiki[:2500] + (wiki[2500:] and '...')



           bot.sendMessage(chat_id=chat_id, text=wiki,reply_to_message_id=msg_id)
           bot.sendMessage(chat_id=chat_id, text="Para ver mas ingresa a: {}".format(url_wiki),reply_to_message_id=msg_id)
       except Exception:
           # Si no encontramos un articulo o hubo algun error
           bot.sendMessage(chat_id=chat_id, text="Hubo un problema con el articulo buscado", reply_to_message_id=msg_id)

   return 'ok'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhook():
    # Usamos el objeto bot para linkear con el chat de la URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))
    # Para ver que todo funcione
    if s:
        return "Webhook ok"
    else:
        return "Webhook fallido"


@app.route('/')
def index():
    return '.'
if __name__ == '__main__':

    app.run(threaded=True)
    
@app.route('/print')
def printMsg():
    wiki = wikipedia.page("Python").content
    info = wiki[:3000] + (wiki[3000:] and '...')
    url_wiki = wikipedia.page("Python").url
    return "Para ver mas ingresa a: {}".format(url_wiki)

if __name__ == '__main__':
    app.run(debug=True)