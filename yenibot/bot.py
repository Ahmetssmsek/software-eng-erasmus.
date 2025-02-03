import pyodbc
import telebot
from telebot import types
import show_aps

# Database connection details
server_name = 'LAPTOP-BETIDGLL'
database_name = 'BOT2'
#username = 'LAPTOP-BETIDGLL'
#password = '178209'

# Establish database connection
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={LAPTOP-BETIDGLL};"
    f"DATABASE={BOT2}
    #f"UID={LAPTOP-BETIDGLL}"
    #f"PWD={178209}"
)

# Telegram token
bot = telebot.TeleBot('6197009456:AAGYdBTjoN1TviR71JisiEznCw3lxJo4Uug')

# Buttons
def create_keyboard(options):
    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    for option in options:
        keyboard.add(types.KeyboardButton(option))
    return keyboard

city = ["Lodz", "Warsaw"]
price = ["Any", "1000 - 1500", "1500 - 2000", "2000 - 2500", "2500 - 3000", "3000 - 3500", "> 3500"]
district = ["Bałuty", "Śródmieście", "Górna", "Widzew", "Polesie"]

# Welcome
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome! Press a button:", reply_markup=create_keyboard(city))

@bot.message_handler(func=lambda message: True)
def setup(message):
    text = "Choose a city:"
    bot.send_message(message.chat.id, text, reply_markup=create_keyboard(city))
    bot.register_next_step_handler(message, choose_city, None, None, None)

def choose_city(message, chosenCity, chosenPrice, chosenDistrict):
    if message.text in city:
        chosenCity = message.text
    
    text = "Choose a price:"
    bot.send_message(message.chat.id, text, reply_markup=create_keyboard(price))
    bot.register_next_step_handler(message, choose_price, chosenCity, None, None)

def choose_price(message, chosenCity, chosenPrice, chosenDistrict):
    if message.text in price:
        chosenPrice = message.text
        
    text = "Choose a district:"
    bot.send_message(message.chat.id, text, reply_markup=create_keyboard(district))
    bot.register_next_step_handler(message, choose_district, chosenCity, chosenPrice, None)

def choose_district(message, chosenCity, chosenPrice, chosenDistrict):
    if message.text in district:
        chosenDistrict = message.text
        
    text = "You chose " + chosenCity + ", " + chosenPrice + ", and " + chosenDistrict + ". Is it correct?"
    bot.send_message(message.chat.id, text, reply_markup=create_keyboard(["Yes", "No"]))
    bot.register_next_step_handler(message, check, chosenCity, chosenPrice, chosenDistrict)

def check(message, chosenCity, chosenPrice, chosenDistrict):
    wrong = False
    if chosenCity is None or chosenDistrict is None or chosenPrice is None:
        bot.send_message(message.chat.id, "Wrong parameters")
        chosenCity = None
        chosenPrice = None
        chosenDistrict = None
        setup(message)
        wrong = True
    if message.text == "No" and not wrong:
        chosenCity = None
        chosenPrice = None
        chosenDistrict = None
        setup(message)
    elif message.text == "Yes" and not wrong:
        resp = show_aps.show(chosenCity, chosenPrice, chosenDistrict)
        for i in reversed(range(len(resp))):
            bot.send_message(message.chat.id, resp[i])

            
bot.polling()