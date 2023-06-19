import requests
import base64
from configparser import ConfigParser
config = ConfigParser()

def generate_image(prompt):
    config.read("conf.ini")
    payload = {
    "prompt": prompt,
    "steps": config["ai"]["steps"],
    "negative_prompt": config["ai"]["defaultnegative"]}
    
    r = requests.post(url=f'http://192.168.2.50:7860/sdapi/v1/txt2img', json=payload).json()
    return base64.b64decode(r['images'][0].split(",",1)[0])