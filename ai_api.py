import requests
import base64
import json
from configparser import ConfigParser

config = ConfigParser()
config.read("conf.ini")
ENDPOINT = config["ai"]["endpoint"]

class BackEndAI():
    def __init__(self) -> None:
        pass
    
    
with open("prestyle.json", "r") as f:
    prestyles = json.load(f)

def apply_prestyles(dictionary, prompt):
    for key, value in dictionary.items():
        prompt = prompt.replace(key, str(value))
    return prompt


def generate_image(prompt):
    config.read("conf.ini")
    prompt = apply_prestyles(prestyles, prompt)
    print(prompt)
    payload = {
    "prompt": prompt,
    "steps": config["ai"]["steps"],
    "cfg_scale": config["ai"]["cfg_scale"],
    "width": config["ai"]["width"],
    "height": config["ai"]["height"],
    "negative_prompt": config["ai"]["defaultnegative"],
    "restore_faces": True}
    
    r = requests.post(url= ENDPOINT + "/sdapi/v1/txt2img", json=payload).json()
    return base64.b64decode(r['images'][0].split(",",1)[0])

def set_steps(steps):
    config.read("conf.ini")
    config.set('ai', 'steps', steps)
    with open('conf.ini', 'w') as config_file:
        config.write(config_file)
    return True

def set_cfg(cfg):
    config.read("conf.ini")
    config.set('ai', 'cfg_scale', cfg)
    with open('conf.ini', 'w') as config_file:
        config.write(config_file)
    return True

def set_res(width, height):
    config.read("conf.ini")
    config.set('ai', 'width', width)
    config.set('ai', 'height', height)
    with open('conf.ini', 'w') as config_file:
        config.write(config_file)
    return True

def get_config():
    config.optionxform = str  # Preserve case sensitivity
    config.read("conf.ini")

    parsed_config = ""

    section = "ai"
    parsed_config += section + ":\n"
    for key, value in config.items(section):
        parsed_config += "\t" + key + ": " + value + "\n"

    return parsed_config

def set_model(model_name):
    r = requests.post(ENDPOINT + "/sdapi/v1/options", json={"sd_model_checkpoint": model_name})
    return True

def get_modes():
    return [model["model_name"] for model in requests.get(url=ENDPOINT + "/sdapi/v1/sd-models").json()]



