import telebot
import pymongo
from pymongo import MongoClient
from bson.json_util import dumps, loads

bot = telebot.TeleBot('5359651293:AAFvhOzi0JTqGMBrKoWYUCcd_XnVR_BCVII')
mongoc = MongoClient('localhost:27017')

@bot.message_handler(content_types=['text'])
def get_text_messages(message):
        global mongoc
        collection = mongoc.meteodata.timeseries
        if message.text == '/help' or message.text == '/start':
                bot.send_message(message.from_user.id, f'/last_record - getting last record from meteostation\n/get_record <time in format: DD/MM/YYYY-HH:MM:SS>')
        elif message.text == '/last_record':
                cursor = collection.find().limit(1).sort("_id", pymongo.DESCENDING)
                cursor_dump = loads(dumps(cursor))[0]
                #print(cursor_dump)
                last_record = f'Time: {cursor_dump["time"]}\nTemperature: {cursor_dump["temperature"]} C\nMoisture: {cursor_dump["moisture"]}%\nPressure: {cursor_dump["pressure"]}'
                bot.send_message(message.from_user.id, last_record)
        elif message.text.startswith('/get_records'):
                if len(message.text.split()) == 2:
                        which_time = message.text.split()[1]
                        cursor = collection.find({'time':which_time})
                        cursor_dump_list = loads(dumps(cursor))
                        if len(cursor_dump_list) == 0:
                                bot.send_message(message.from_user.id, 'No such records')
                        else:
                                for cursor_dump in cursor_dump_list:
                                        record = f'Time: {cursor_dump["time"]}\nTemperature: {cursor_dump["temperature"]} C\nMoisture: {cursor_dump["moisture"]}%\nPressure: {cursor_dump["pressure"}'
                                        bot.send_message(message.from_user.id, record)
        else:
                bot.send_message(message.from_user.id, 'I do not understand you. Write /help for directions for use')

bot.polling(none_stop=True, interval=0)
