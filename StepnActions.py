import os
import yaml
from yaml import CLoader as Loader
import base64
import hmac
import time
import requests
import stepn_password
import json

with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as config_file:
    config = yaml.load(config_file, Loader=Loader)
    acc = config.get('StepnAccount')
    secret = config.get('GoogleSecret')



class StepnActions:
    def __init__(self):
        self.sessionID = self.log_in()

    def get_acc_inf(self, chain: int) -> json:
        URL = 'https://api.stepn.com/run/userbasic?sessionID='
        if chain not in [101, 103, 104]:
            raise ValueError("chain must be one of 101, 103, 104")
        connection = requests.get(URL + self.sessionID)
        api_content = connection.content
        data = json.loads(api_content).get('data')
        if not data:
            return None

        asset = [i for i in data['asset'] if i['chain'] == chain]
        result_values = {}

        if chain == 101:
            result_values['eth'] = [i['value'] / 1000000 for i in asset if i['token'] == 1001]
            result_values['eth'] = result_values['eth'][0] if result_values['eth'] else ''

        if chain == 103:
            result_values['sol'] = [i['value'] / 1000000 for i in asset if i['token'] == 1003]
            result_values['sol'] = result_values['sol'][0] if result_values['sol'] else ''

        if chain == 104:
            result_values['bnb'] = [i['value'] / 1000000 for i in asset if i['token'] == 1004]
            result_values['bnb'] = result_values['bnb'][0] if result_values['bnb'] else ''

        result_values['gst'] = [i['value'] / 100 for i in asset if i['token'] == 3000]
        result_values['gst'] = result_values['gst'][0] if result_values['gst'] else ''

        result_values['gmt'] = [i['value'] / 100 for i in asset if i['token'] == 3001]
        result_values['gmt'] = result_values['gmt'][0] if result_values['gmt'] else ''

        return result_values

    def get_shoe_list(self,chain: int):
        URL = 'https://api.stepn.com/run/shoelist?sessionID='
        if chain not in [101, 103, 104]:
            raise ValueError("chain must be one of 101, 103, 104")
        connection = requests.get(URL + self.sessionID)
        api_content = connection.content
        data = json.loads(api_content).get('data')
        if not data:
            return None

        sneakers = []
        for i in data:
            sneaker_data = {}
            if i['chain'] == chain:
                sneaker_data['otd'] = i['otd']
                sneaker_data['level'] = i['level']
                sneaker_data['breed'] = i['breed']
                sneaker_data['shoeImg'] = 'https://res.stepn.com/imgOut/'+i['shoeImg']
                attrs = i['attr']
                totalAttrs = i['totalAttr']
                sneaker_data['attrs'] = {
                    'baseEfficiency' : float(attrs[0])/10,
                    'baseLuck' : float(attrs[1])/10,
                    'baseComfort' : float(attrs[2])/10,
                    'baseResilience' : float(attrs[3])/10,
                    'Efficiency' : float(totalAttrs[0])/10,
                    'Luck' : float(totalAttrs[1])/10,
                    'Comfort' : float(totalAttrs[2])/10,
                    'Resilience' : float(totalAttrs[3])/10
                }
                sneakers.append(sneaker_data)

        return sneakers



    def log_in(self) -> str:
        hashed_password = stepn_password.hash_password(acc['login'], acc['password'])
        con = requests.get(
            f'https://api.stepn.com/run/login?account=ruslannagnibedaa%40gmail.com&password={hashed_password}&type=3&deviceInfo=web')
        content = con.content
        data = json.loads(content)['data']
        sessionID = data['sessionID'].replace(':', '%3A')
        requests.get(f'https://api.stepn.com/run/doCodeCheck?codeData=2%3A{self.google_code}&sessionID={sessionID}')

        return sessionID

    @property
    def google_code(self) -> str:
        key = base64.b32decode(secret, True)
        now = int(time.time() // 30)
        msg = now.to_bytes(8, "big")
        digest = hmac.new(key, msg, "sha1").digest()
        offset = digest[19] & 0xF
        code = digest[offset: offset + 4]
        code = int.from_bytes(code, "big") & 0x7FFFFFFF
        code = code % 1000000
        return "{:06d}".format(code)


actions = StepnActions()
print(actions.get_shoe_list(103))
print(actions.get_acc_inf(103))