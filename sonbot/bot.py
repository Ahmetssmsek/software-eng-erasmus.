import pyodbc
import telebot
from telebot import types
import show_aps

# Database connection details
server_name = 'LAPTOP-BETIDGLL'
database_name = 'BOT2'
#username = 'projectt'
#password = 'project'

# Establish database connection
conn = pyodbc.connect(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={server_name};"
    f"DATABASE={database_name};"
  #  f"UID={username};"
   # f"PWD={password}"
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
        for item in resp:
            insert_data(item)
            bot.send_message(message.chat.id, item)

def insert_data(item):
    # Perform SQL insert operation here using the connection (conn) and the item data
    cursor = conn.cursor()
    # Assuming you have a table called 'YourTableName' with appropriate columns
    query = f"INSERT INTO LodzDB2 (Title, District, Price,Rooms, Area,Time_added, Link) VALUES (?, ?, ?, ?, ?, ?, ?)"
    cursor.execute(query, item)  # Replace column1, column2, column3 with your actual column names
    conn.commit()

bot.polling()