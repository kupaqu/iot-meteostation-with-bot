mport telebot
from telebot import types
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps, loads
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import random

bot = telebot.TeleBot('5359651293:AAFvhOzi0JTqGMBrKoWYUCcd_XnVR_BCVII')
mongoc = MongoClient('localhost:27017')

keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
keyboard.add('/last_record')
keyboard.add('/plot')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
        global mongoc
        collection = mongoc.meteodata.timeseries
        if message.text == '/help' or message.text == '/start':
                bot.send_message(message.from_user.id, f'/plot - plot the last 360 records\n/last_record - getting last record from meteostation\n/get_record <time in format: DD/MM/YYYY-HH:MM:SS>', reply_markup=keyboard)
        elif message.text == '/last_record':
                cursor = collection.find().limit(1).sort("_id", pymongo.DESCENDING)
                cursor_dump = loads(dumps(cursor))[0]
                #print(cursor_dump)
                last_record = f'Time: {cursor_dump["time"]}\nTemperature: {cursor_dump["temperature"]} C\nMoisture: {cursor_dump["moisture"]}%\nPressure: {cursor_dump["pressure"]}'
                bot.send_message(message.from_user.id, last_record)
        elif message.text.startswith('/get_record'):
                if len(message.text.split()) == 2:
                        which_time = message.text.split()[1]
                        cursor = collection.find({'time':which_time})
                        cursor_dump_list = loads(dumps(cursor))
                        if len(cursor_dump_list) == 0:
                                bot.send_message(message.from_user.id, 'No such records')
                        else:
                                for cursor_dump in cursor_dump_list:
                                        record = f'Time: {cursor_dump["time"]}\nTemperature: {cursor_dump["temperature"]} C\nMoisture: {cursor_dump["moisture"]}%\nPressure: {cursor_dump["pressure"]}'
                                        bot.send_message(message.from_user.id, record)
        elif message.text == '/plot':
                cursor = collection.find().limit(360).sort("_id", pymongo.DESCENDING)
                cursor_dump = loads(dumps(cursor))
                df = pd.DataFrame(cursor_dump)
                figure, axis = plt.subplots(3, 1)
                axis[0].plot(df['temperature'])
                axis[0].set_title('Temperature')
                axis[1].plot(df['moisture'])
                axis[1].set_title('Moisture')
                axis[2].plot(df['pressure'])
                axis[2].set_title('Pressure')
                now = datetime.now()
                filename = f'/home/kupaqu/{now.strftime("%d%m%Y_%H%M%S")}_{random.randint(0, 100)}.png'
                figure.savefig(filename)
                plt.close(figure)
                bot.send_photo(message.from_user.id, open(filename, 'rb'))
                bot.send_message(message.from_user.id, f'Start time is {df["time"].iloc[-1]}\nEnd time is {df["time"].iloc[0]}')
        else:
                bot.send_message(message.from_user.id, 'I do not understand you. Write /help for directions for use')

bot.polling(none_stop=True, interval=0)
