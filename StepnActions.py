import os
import yaml
from yaml import CLoader as Loader
import base64
import hmac
import time
import requests
import stepn_password
import json
from loguru import logger
from collections import OrderedDict

from Exceptions import InauthorizedAccount
from SneakerFind import SneakerFind



with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as config_file:
    config = yaml.load(config_file, Loader=Loader)
    acc = config.get('StepnAccount')
    secret = config.get('GoogleSecret')


class StepnActions:
    def __init__(self):
        self.sessionID = self.log_in()

    def log_in(self) -> str:
        while True:
            try:
                hashed_password = stepn_password.hash_password(acc['login'], acc['password'])
                con = requests.get(
                    f'https://api.stepn.com/run/login?account=ruslannagnibedaa%40gmail.com&password={hashed_password}&type=3&deviceInfo=web')
                content = con.content
                data = json.loads(content)
                data = data['data']
                sessionID = data['sessionID'].replace(':', '%3A')
                code_check = requests.get(f'https://api.stepn.com/run/doCodeCheck?codeData=2%3A{self.google_code}&sessionID={sessionID}')
                code_check_content = json.loads(code_check.content)
                try:
                    if code_check_content['code'] == 101033:
                         requests.get(f'https://api.stepn.com/run/doCodeCheck?codeData=2%3A{self.google_code}&sessionID={sessionID}')
                         logger.warning('incorrect google_code')
                except Exception as e:
                    logger.warning(e)
                break
            except Exception as e:
                logger.warning(e)
                time.sleep(10)

        logger.warning('logging in')
        self.sessionID = sessionID
        return sessionID

    def get_acc_inf(self, chain: int) -> json:
        URL = 'https://api.stepn.com/run/userbasic?sessionID='
        if chain not in [101, 103, 104]:
            raise ValueError("chain must be one of 101, 103, 104")
        connection = requests.get(URL + self.sessionID)
        api_content = connection.content
        data = json.loads(api_content)
        code = data.get('code', None)
        if code == 102001:
            self.log_in()
            connection = requests.get(URL + self.sessionID)
            api_content = connection.content
            data = json.loads(api_content)
        data = data['data']
        if not data:
            return None

        asset = [i for i in data['asset'] if i['chain'] == chain]
        result_values = {}

        if chain == 101:
            result_values['eth'] = [i['value'] / 1000000 for i in asset if i['token'] == 1001]
            result_values['eth'] = result_values['eth'][0] if result_values['eth'] else 0

        if chain == 103:
            result_values['sol'] = [i['value'] / 1000000 for i in asset if i['token'] == 1003]
            result_values['sol'] = result_values['sol'][0] if result_values['sol'] else 0

        if chain == 104:
            result_values['bnb'] = [i['value'] / 1000000 for i in asset if i['token'] == 1004]
            result_values['bnb'] = result_values['bnb'][0] if result_values['bnb'] else 0

        result_values['gst'] = [i['value'] / 100 for i in asset if i['token'] == 3000]
        result_values['gst'] = result_values['gst'][0] if result_values['gst'] else 0

        result_values['gmt'] = [i['value'] / 100 for i in asset if i['token'] == 3001]
        result_values['gmt'] = result_values['gmt'][0] if result_values['gmt'] else 0

        logger.info('getting acc info')
        return result_values

    def get_shoe_list(self, chain: int):
        URL = 'https://api.stepn.com/run/shoelist?sessionID='
        if chain not in [101, 103, 104]:
            raise ValueError("chain must be one of 101, 103, 104")
        connection = requests.get(URL + self.sessionID)
        api_content = connection.content
        data = json.loads(api_content)
        code = data.get('code', None)
        if code == 102001:
            self.log_in()
            connection = requests.get(URL + self.sessionID)
            api_content = connection.content
            data = json.loads(api_content)
        data = data['data']
        if not data:
            return None

        sneakers = []
        for i in data:
            sneaker_data = {}
            if i['chain'] == chain:
                sneaker_data['otd'] = i['otd']
                sneaker_data['level'] = i['level']
                sneaker_data['breed'] = i['breed']
                sneaker_data['shoeImg'] = 'https://res.stepn.com/imgOut/' + i['shoeImg']
                attrs = i['attr']
                totalAttrs = i['totalAttr']
                sneaker_data['attrs'] = {
                    'baseEfficiency': float(attrs[0]) / 10,
                    'baseLuck': float(attrs[1]) / 10,
                    'baseComfort': float(attrs[2]) / 10,
                    'baseResilience': float(attrs[3]) / 10,
                    'Efficiency': float(totalAttrs[0]) / 10,
                    'Luck': float(totalAttrs[1]) / 10,
                    'Comfort': float(totalAttrs[2]) / 10,
                    'Resilience': float(totalAttrs[3]) / 10
                }
                sneakers.append(sneaker_data)

        logger.info('getting shoe list')
        return sneakers


    def check_sold(self, otd: int) -> str:
        URL = 'https://api.stepn.com/run/shoelist?sessionID='
        connection = requests.get(URL + self.sessionID)
        api_content = connection.content
        data = json.loads(api_content)
        code = data.get('code', None)
        if code == 102001:
            self.log_in()
            connection = requests.get(URL + self.sessionID)
            api_content = connection.content
            data = json.loads(api_content)
        data = data['data']
        if not data:
            return True

        for i in data:
            if i['otd'] == otd:
                return False


        logger.info('checking sales')
        return True


    def buy_sneaker(self, orderID: str, price: str):
        sneaker_buy_url = f"https://api.stepn.com/run/buyprop?orderID={orderID}&price={price}&googleCode=&sessionID={self.sessionID}&"
        sneaker_data = requests.get(sneaker_buy_url).content
        data = json.loads(sneaker_data)
        code = data.get('code', None)
        if code == 102001:
            self.log_in()
            sneaker_buy_url = f"https://api.stepn.com/run/buyprop?orderID={orderID}&price={price}&googleCode=&sessionID={self.sessionID}&"
            sneaker_data = requests.get(sneaker_buy_url).content
            data = json.loads(sneaker_data)

        return data

    def get_order_inf(self, orderID: str):
        order_inf_url = f"https://api.stepn.com/run/orderdata?orderId={orderID}&sessionID="
        api_content = requests.get(order_inf_url+self.sessionID).content
        data = json.loads(api_content)
        code = data.get('code', None)
        if code == 102001:
            self.log_in()
            connection = requests.get(order_inf_url+self.sessionID)
            api_content = connection.content
            data = json.loads(api_content)
        if code == 212017:
            return data['msg']

        content = data['data']

        sneaker_data = {}
        sneaker_data['otd'] = content['otd']
        sneaker_data['level'] = content['level']
        sneaker_data['breed'] = content['breed']
        sneaker_data['shoeImg'] = 'https://res.stepn.com/imgOut/' + content['shoeImg']
        attrs = content['attrs']
        sneaker_data['attrs'] = {
            'baseEfficiency': float(attrs[0]) / 10,
            'baseLuck': float(attrs[1]) / 10,
            'baseComfort': float(attrs[2]) / 10,
            'baseResilience': float(attrs[3]) / 10 }

        return sneaker_data

    def get_first_ten_sneakers(self, project_id):
        res = []
        find_sneaker_obj = SneakerFind(project_id)
        while True:
            try:
                sneakers = find_sneaker_obj.get_sneakers_from_pages(self.sessionID, 1)[:10]
            except InauthorizedAccount:
                self.log_in()
            else:
                break


        for sneaker in sneakers:
            sneaker_data = OrderedDict()
            sneaker_data['otd'] = sneaker['otd']
            sneaker_data['level'] = sneaker['level']
            sneaker_data['mint'] = sneaker['mint']
            sneaker_data['chain'] = find_sneaker_obj.chain
            sneaker_data['price'] = float(sneaker['sellPrice']) / 1000000
            sneaker_data['img'] = 'https://res.stepn.com/imgOut/' + sneaker['img']
            sneaker_data['attrs'] = {
                'Efficiency': float(sneaker['v1']) / 10,
                'Luck': float(sneaker['v2']) / 10}
            res.append(sneaker_data)

        return res

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
