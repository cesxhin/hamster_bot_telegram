"""
package request:
1. requests
2. telebot
"""

from time import sleep
import requests
import os, json, random
import telebot

#settings variables
global bot
global TOKEN
global imagesAPI
#read file of configuration for this app
absolute_dir = os.path.dirname(__file__)
nameFile = "settings.json"
file = open(os.path.join(absolute_dir, nameFile))
dataJson = json.load(file)
#set token for telegram
TOKEN = dataJson['bot_token']
ImageAuth = dataJson['ImageAuth']
#set token for api images
imagesAPI = "https://api.pexels.com/v1/search?query=hamster"

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def handle_command_start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=4)
    itemHamster = telebot.types.KeyboardButton('/🐹')
    markup.add(itemHamster)
    bot.send_message(message.chat.id, "Hello, welcome to Telegram Bot!", reply_markup=markup)


@bot.message_handler(commands=['🐹'])
def handle_command_hamster(messages):
    #get photo
    url = getUrlPhoto()
    
    #send photo
    print("Chat id:"+str(messages.chat.id) +" get url -> "+url['src']['original'])
    try:
        bot.send_photo(messages.chat.id, str(url['src']['small']), reply_to_message_id=messages.message_id)
    except:
        bot.send_message(messages.chat.id, "error generic, try again please", reply_to_message_id=messages.message_id)

def getUrlPhoto():
    response = requests.get(imagesAPI, headers={"Authorization": ImageAuth}).json()
    totalResults = response['total_results']
    perPage = response['per_page']

    #random
    page = random.randint(1, int(totalResults/perPage))
    imagePos = random.randint(0, 14)

    #get list photos
    listImages = requests.get(imagesAPI+"&page="+str(page), headers={"Authorization": ImageAuth}).json()

    #check overflow
    if imagePos > (len(listImages['photos'])-1):
        return listImages['photos'][len(listImages['results'])-1]
    else:
        return listImages['photos'][imagePos]

bot.polling()
