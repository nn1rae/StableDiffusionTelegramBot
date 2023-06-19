from dotenv import load_dotenv
from os import getenv
import requests
import json
import requests
import io
import base64
from PIL import Image, PngImagePlugin
import logging
from aiogram import Bot, Dispatcher, executor, types
from configparser import ConfigParser

import keyboard


config = ConfigParser()


load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=getenv("API_TOKEN"))
dp = Dispatcher(bot)


    
    
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.answer("Successfull")
    
    
@dp.message_handler(commands=['gen'])
async def send_welcome(message: types.Message):
    args = message.get_args()
    config.read("conf.ini")
    logging.info(f"{message.from_user.full_name} /gen {args}")
    payload = {
    "prompt": "".join(args),
    "steps": config["ai"]["steps"],
    "negative_prompt": config["ai"]["defaultnegative"]}
    
    r = requests.post(url=f'http://192.168.2.50:7860/sdapi/v1/txt2img', json=payload).json()
    for i in r['images']:
        await bot.send_photo(message.chat.id, base64.b64decode(i.split(",",1)[0]), reply_markup=keyboard.generate([["try again", "redo:" + "".join(args)]]))
    
    
@dp.message_handler(commands=['steps'])
async def send_welcome(message: types.Message):
    args = message.get_args().split(" ")
    if len(args) == 1 and args[0].isdigit():
        config.read("conf.ini")
        config.set('ai', 'steps', args[0])
        with open('conf.ini', 'w') as config_file:
            config.write(config_file)
        logging.info(f"{message.from_user.full_name} set steps to {args[0]}")
        await bot.send_message(message.chat.id, "success")
    else:
        
        logging.warning(f"{message.from_user.full_name} /steps {args}")
        await bot.send_message(message.chat.id, "Wrong fromat, this will be reported")
        
        
@dp.callback_query_handler()
async def claabackfunc(callback: types.CallbackQuery):
    comand, args = callback.data.split(":", maxsplit=1)
    match comand:
        case "redo":
            pass
        case _:
            pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)