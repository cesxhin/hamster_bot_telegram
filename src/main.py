from time import sleep
import requests
import os, json, random
import telebot

#settings variables
global bot
global imagesAPI

#read file of configuration for this app
absolute_dir = os.path.dirname(__file__)
nameFile = "settings.json"
file = open(os.path.join(absolute_dir, nameFile))
dataJson = json.load(file)

#set token for telegram
TOKEN = dataJson['bot_token']
ImageAuth = dataJson['imageAuth']

#set token for api images
imagesAPI = "https://pixabay.com/api/?image_type=photo&category=animals&q=hamster&key="+ImageAuth

#set token for bot
bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def handle_command_start(message):
    markup = telebot.types.ReplyKeyboardMarkup(row_width=4)
    itemHamster = telebot.types.KeyboardButton('🐹')
    markup.add(itemHamster)
    bot.send_message(message.chat.id, "Hi, welcome to Hamster Bot! Send this emoji '🐹' and you'll recive a hamster photo", reply_markup=markup)


@bot.message_handler(regexp="🐹")
def handle_command_hamster(messages):
    #get photo
    url = getUrlPhoto()
    
    #send photo
    print("Chat id:"+str(messages.chat.id) +" get url -> "+url['webformatURL'])
    try:
        bot.send_photo(messages.chat.id, str(url['webformatURL']), reply_to_message_id=messages.message_id)
    except:
        bot.send_message(messages.chat.id, "error generic, try again please", reply_to_message_id=messages.message_id)

def getUrlPhoto():
    response = requests.get(imagesAPI).json()
    totalResults = response['totalHits']
    perPage = 20

    #random
    page = random.randint(1, int(totalResults/perPage))
    imagePos = random.randint(0, 14)

    #get list photos
    listImages = requests.get(imagesAPI+"&page="+str(page)).json()

    #check overflow
    if imagePos > (len(listImages['hits'])-1):
        return listImages['hits'][len(listImages['hits'])-1]
    else:
        return listImages['hits'][imagePos]

bot.polling()
