from dotenv import load_dotenv
from os import getenv
import logging
from aiogram import Bot, Dispatcher, executor, types
from configparser import ConfigParser
from AIBackEndAPI import BackEndAI
import keyboard

load_dotenv()

ai = BackEndAI()
config = ConfigParser()
bot = Bot(token=getenv("API_TOKEN"))
dp = Dispatcher(bot)


logging.basicConfig(level=logging.INFO)



@dp.message_handler(commands=['help'])
async def message_handler(message: types.Message):
    text = """Generate image /gen [prompt]
set steps /steps (steps)
set cfg scale /cfg (cfg scale)
set resolution /res (width) (height)
set model /models
get corrent configuration /config
set sampler /sampler
    """
    await message.answer(text)
    await bot.delete_message(message.chat.id, message.message_id)
    
@dp.message_handler(commands=['start'])
async def message_handler(message: types.Message):
    await message.answer("Successfull")
    
    
# Use in case u want to hendle generation by comand hangler, if uncomment comment message handler below V
 
#@dp.message_handler(commands=['gen'])
#async def message_handler(message: types.Message):
#    prompt = "".join(message.get_args())
#    logging.info(f"{message.from_user.full_name} /gen {prompt}")
#    await bot.send_photo(message.chat.id, ai.generate_image(prompt))
    

@dp.message_handler()
async def message_handler(message: types.Message):
    prompt = message.text
    logging.info(f"{message.from_user.full_name} {prompt}")
    await bot.send_photo(message.chat.id, ai.generate_image(prompt))
    
    
        
    
@dp.message_handler(commands=['steps'])
async def message_handler(message: types.Message):
    args = message.get_args().split(" ")
    if len(args) == 1 and args[0].isdigit():
        ai.set_steps(args[0])
        logging.info(f"{message.from_user.full_name} set steps to {args[0]}")
        await bot.delete_message(message.chat.id, message.message_id)
    else:
        
        logging.warning(f"{message.from_user.full_name} /steps {args}")
        await bot.send_message(message.chat.id, "Wrong fromat, this will be reported")
        
@dp.message_handler(commands=['cfg'])
async def message_handler(message: types.Message):
    args = message.get_args().split(" ")
    if len(args) == 1 and args[0].isdigit():
        ai.set_cfg(args[0])
        logging.info(f"{message.from_user.full_name} set cfg to {args[0]}")
        await bot.delete_message(message.chat.id, message.message_id)
    else:
        
        logging.warning(f"{message.from_user.full_name} /cfg {args}")
        await bot.send_message(message.chat.id, "Wrong fromat, this will be reported")
        
@dp.message_handler(commands=['res'])
async def message_handler(message: types.Message):
    try: 
        width, height = message.get_args().split(maxsplit=1)
        if width.isdigit() and height.isdigit():
            ai.set_res(width, height)
            logging.info(f"{message.from_user.full_name} set res to {message.get_args()}")
            await bot.delete_message(message.chat.id, message.message_id)
        else:
            
            logging.warning(f"{message.from_user.full_name} /res {message.get_args()}")
            await bot.send_message(message.chat.id, "Wrong fromat, this will be reported")
    except:
        pass

@dp.message_handler(commands=['models'])
async def message_handler(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer("Available models:", reply_markup=keyboard.generate([[model_name, "change_model:" + model_name] for model_name in ai.get_modes()]))
    
@dp.message_handler(commands=['sampler'])
async def message_handler(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await message.answer("Available samplers:", reply_markup=keyboard.generate([[sampler, "change_sampler:" + sampler] for sampler in ai.get_samplers()]))
    
@dp.message_handler(commands=['config'])
async def message_handler(message: types.Message):
    await bot.delete_message(message.chat.id, message.message_id)
    await bot.send_message(message.chat.id, ai.get_config())
        
@dp.callback_query_handler()
async def claabackfunc(callback: types.CallbackQuery):
    comand, args = callback.data.split(":", maxsplit=1)
    match comand:
        case "prompt":
            await bot.send_message(callback.from_user.id, args)
        case "change_model":
            ai.set_model(args)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        case "change_sampler":
            ai.set_sampler(args)
            await bot.delete_message(callback.message.chat.id, callback.message.message_id)
        case _:
            pass

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)