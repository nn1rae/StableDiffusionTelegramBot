import requests
import base64
import json
from configparser import ConfigParser



class BackEndAI():
    def __init__(self) -> None:
        self.config = ConfigParser()
        self.config.read("conf.ini")
        self.ENDPOINT = self.config["ai"]["endpoint"]
        
        with open("prestyle.json", "r") as f:
            self.prestyles = json.load(f)

    def _apply_prestyles(self, prompt):
        for key, value in self.prestyles.items():
            prompt = prompt.replace(key, str(value))
        return prompt


    def generate_image(self, prompt):
        self.config.read("conf.ini")
        prompt = self._apply_prestyles(prompt)
        payload = {
        "prompt": prompt,
        "steps":  self.config["ai"]["steps"],
        "cfg_scale":  self.config["ai"]["cfg_scale"],
        "width":  self.config["ai"]["width"],
        "height":  self.config["ai"]["height"],
        "negative_prompt":  self.config["ai"]["defaultnegative"],
        "restore_faces": True}
        
        r = requests.post(url= self.ENDPOINT + "/sdapi/v1/txt2img", json=payload).json()
        return base64.b64decode(r['images'][0].split(",",1)[0])

    def set_steps(self,steps):
        self.config.read("conf.ini")
        self.config.set('ai', 'steps', steps)
        with open('conf.ini', 'w') as config_file:
            self.config.write(config_file)
        return True

    def set_cfg(self,cfg):
        self.config.read("conf.ini")
        self.config.set('ai', 'cfg_scale', cfg)
        with open('conf.ini', 'w') as config_file:
            self.config.write(config_file)
        return True

    def set_res(self,width, height):
        self.config.read("conf.ini")
        self.config.set('ai', 'width', width)
        self.config.set('ai', 'height', height)
        with open('conf.ini', 'w') as config_file:
            self.config.write(config_file)
        return True

    def get_config(self):
        self.config.optionxform = str  # Preserve case sensitivity
        self.config.read("conf.ini")

        parsed_config = ""

        section = "ai"
        parsed_config += section + ":\n"
        for key, value in self.config.items(section):
            parsed_config += "\t" + key + ": " + value + "\n"

        return parsed_config

    def set_model(self,model_name):
        r = requests.post(self.ENDPOINT + "/sdapi/v1/options", json={"sd_model_checkpoint": model_name})
        return True

    def get_modes(self):
        return [model["model_name"] for model in requests.get(url=self.ENDPOINT + "/sdapi/v1/sd-models").json()]



