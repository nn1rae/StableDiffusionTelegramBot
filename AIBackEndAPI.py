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
        HiresFix_payload = {
        "enable_hr": "true",
        "denoising_strength": 0.7,
        "firstphase_width": self.config["ai"]["width"],
        "firstphase_height": self.config["ai"]["height"],
        "hr_scale": 2,
        "hr_upscaler": "SwinIR_4x",
        "hr_second_pass_steps": self.config["ai"]["steps"],
        "hr_resize_x": 0,
        "hr_resize_y": 0,
        "hr_sampler_name": self.config["ai"]["sampler"],
        "hr_prompt": prompt,
        "hr_negative_prompt": self.config["ai"]["defaultnegative"]
        }
        payload = {        
        "seed": -1,
        "prompt": prompt,
        "steps":  self.config["ai"]["steps"],
        "cfg_scale":  self.config["ai"]["cfg_scale"],
        "width":  self.config["ai"]["width"],
        "height":  self.config["ai"]["height"],
        "negative_prompt":  self.config["ai"]["defaultnegative"],
        "sampler_index": self.config["ai"]["sampler"],
        "restore_faces": self.config["ai"]["restorefaces"]}
        
        if self.config["ai"]["hiresfix"] == "true":
            payload.update(HiresFix_payload)
            
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
    
    def get_samplers(self):
        return [sampler["name"] for sampler in requests.get(url=self.ENDPOINT + "/sdapi/v1/samplers").json()]
    
    def set_sampler(self, sampler):
        self.config.read("conf.ini")
        self.config.set('ai', 'sampler', sampler)
        with open('conf.ini', 'w') as config_file:
            self.config.write(config_file)
        return True
    
    
    
    def upscale_photo(self, image_path):
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
            
        payload = {
    "resize_mode": 0,
    "show_extras_results": True,
    "gfpgan_visibility": 1,
    "codeformer_visibility": 0,
    "codeformer_weight": 0,
    "upscaling_resize": 4,
    "upscaling_resize_w": 512,
    "upscaling_resize_h": 512,
    "upscaling_crop": True,
    "upscaler_1": "SwinIR_4x",
    "upscaler_2": "None",
    "extras_upscaler_2_visibility": 0,
    "upscale_first": False,
    "image": image_data
    }
        r = requests.post(url= self.ENDPOINT + "/sdapi/v1/extra-single-image", json=payload).json()
        return base64.b64decode(r['image'])
    
    def set_restorefaces(self,data):
        self.config.read("conf.ini")
        self.config.set('ai', 'restorefaces', data)
        with open('conf.ini', 'w') as config_file:
            self.config.write(config_file)
        return True
    
    def set_hiresfix(self,data):
        self.config.read("conf.ini")
        self.config.set('ai', 'hiresfix', data)
        with open('conf.ini', 'w') as config_file:
            self.config.write(config_file)
        return True

    
        




