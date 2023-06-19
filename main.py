from dotenv import load_dotenv
from os import getenv
import logging
from aiogram import Bot, Dispatcher, executor, types
from configparser import ConfigParser
import ai_api

import keyboard


config = ConfigParser()


load_dotenv()

logging.basicConfig(level=logging.INFO)

bot = Bot(token=getenv("API_TOKEN"))
dp = Dispatcher(bot)


    
    
@dp.message_handler(commands=['start'])
async def message_handler(message: types.Message):
    await message.answer("Successfull")
    
    
@dp.message_handler(commands=['gen'])
async def message_handler(message: types.Message):
    prompt = "".join(message.get_args())
    logging.info(f"{message.from_user.full_name} /gen {prompt}")
    await bot.send_photo(message.chat.id, ai_api.generate_image(prompt), reply_markup=keyboard.generate([["try again", "redo:" + prompt]]))
    
    
@dp.message_handler(commands=['steps'])
async def message_handler(message: types.Message):
    args = message.get_args().split(" ")
    if len(args) == 1 and args[0].isdigit():
        ai_api.set_steps(args[0])
        logging.info(f"{message.from_user.full_name} set steps to {args[0]}")
        await bot.send_message(message.chat.id, "success")
    else:
        
        logging.warning(f"{message.from_user.full_name} /steps {args}")
        await bot.send_message(message.chat.id, "Wrong fromat, this will be reported")
        
@dp.message_handler(commands=['cfg'])
async def message_handler(message: types.Message):
    args = message.get_args().split(" ")
    if len(args) == 1 and args[0].isdigit():
        ai_api.set_cfg(args[0])
        logging.info(f"{message.from_user.full_name} set cfg to {args[0]}")
        await bot.send_message(message.chat.id, "success")
    else:
        
        logging.warning(f"{message.from_user.full_name} /cfg {args}")
        await bot.send_message(message.chat.id, "Wrong fromat, this will be reported")
        
@dp.message_handler(commands=['res'])
async def message_handler(message: types.Message):
    try: 
        width, height = message.get_args().split(maxsplit=1)
        if width.isdigit() and height.isdigit():
            ai_api.set_res(width, height)
            logging.info(f"{message.from_user.full_name} set res to {message.get_args()}")
            await bot.send_message(message.chat.id, "success")
        else:
            
            logging.warning(f"{message.from_user.full_name} /res {message.get_args()}")
            await bot.send_message(message.chat.id, "Wrong fromat, this will be reported")
    except:
        pass
    
@dp.message_handler(commands=['config'])
async def message_handler(message: types.Message):
    await bot.send_message(message.chat.id, ai_api.get_config())
        
@dp.callback_query_handler()
async def claabackfunc(callback: types.CallbackQuery):
    comand, args = callback.data.split(":", maxsplit=1)
    match comand:
        case "redo":
            logging.info(f"{callback.from_user.full_name} /gen {args}")
            await bot.send_photo(callback.from_user.id, ai_api.generate_image(args), reply_markup=keyboard.generate([["try again", "redo:" + args]]))
        case _:
            pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)