import json
import requests
from DB import DB


class SneakerFind:
    def __init__(self, project_id):
        self.db = DB()
        filters = self.db.get_filters(project_id)
        chain = self.db.get_chain(project_id)
        self.sneakers_types = ['Sneakers', 'Shoeboxes']
        self.sneakers_rarities = ['Genesis', 'OG']
        self.qualities = ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary']
        self.sneakers_classes = ['Walker', 'Jogger', 'Runner', 'Trainer']
        self.pages = ['Gems', 'Others']
        self.gem_types = ['Efficiency', 'Luck', 'Comfort', 'Resilience']
        self.api_url_obj = ApiUrl()
        self.api_url_obj.set_chain(chain)
        self._set_filters(list(filters)[0], **filters[list(filters)[0]])

    def parse_lvls_from_str(self, string: str) -> tuple[int, int]:
        string = string.split('-')
        lvls = []
        for i in string:
            lvls.append(int(i.replace(' ', '')))
        return lvls[0], lvls[1]

    def _set_filters(self, section: str, **kwargs) -> None:

        if section == 'Sneakers':
            type = kwargs['Type'] if 'Type' in kwargs else None
            if type == 'Shoeboxes':
                if type not in self.sneakers_types:
                    raise ValueError('Unknown type')
                self.api_url_obj.set_all_type(type)

                quality = kwargs['Quality'] if 'Quality' in kwargs else None
                if quality:
                    if quality not in self.qualities:
                        raise ValueError('Unknown quality')
                    self.api_url_obj.set_quality(quality)

            if type == 'Sneakers':
                if type not in self.sneakers_types:
                    raise ValueError('Unknown type')
                self.api_url_obj.set_all_type(type)

                rarity = kwargs['Rarity'] if 'Rarity' in kwargs else None
                if rarity:
                    if rarity not in self.sneakers_rarities:
                        raise ValueError('Unknown rarity')
                    self.api_url_obj.set_sneakers_rarity(rarity)

                _class = kwargs['Class'] if 'Class' in kwargs else None
                if _class:
                    if _class not in self.sneakers_classes:
                        raise ValueError('Unknown class')
                    self.api_url_obj.set_sneakers_class(_class)

                quality = kwargs['Quality'] if 'Quality' in kwargs else None
                if quality:
                    if quality not in self.qualities:
                        raise ValueError('Unknown quality')
                    self.api_url_obj.set_quality(quality)

                lvl = kwargs['Level'] if 'Level' in kwargs else None
                if lvl:
                    lvl_min, lvl_max = self.parse_lvls_from_str(lvl)

                    if lvl_min > 30 or lvl_min < 0 or lvl_max < 0 or lvl_max > 30:
                        raise ValueError("sneakers lvls must be between 0 and 30")
                    if lvl_min > lvl_max:
                        raise ValueError("min sneakers lvls value > max sneakers lvls value")

                    self.api_url_obj.set_sneakers_lvl(lvl_min, lvl_max)

                shoe_mint = kwargs['Shoe mint'] if 'Shoe mint' in kwargs else None
                if shoe_mint:
                    shoe_min, shoe_max = self.parse_lvls_from_str(shoe_mint)

                    if shoe_min > 7 or shoe_min < 0 or shoe_max < 0 or shoe_max > 7:
                        raise ValueError("sneakers shoe mint must be between 0 and 7")
                    if shoe_min > shoe_max:
                        raise ValueError("min sneakers shoe mint value > max sneakers shoe mint value")
                    self.api_url_obj.set_sneakers_shoe_mint(shoe_min, shoe_max)

            elif section == 'Gems':
                if section not in self.pages:
                    raise ValueError(f"Invalid page: {section}")
                self.api_url_obj.set_page(section)

                type = kwargs['Type'] if 'Type' in kwargs else None
                if type:
                    if type not in self.gem_types:
                        raise ValueError(f"Invalid gem type: {type}")
                    self.api_url_obj.set_gems_type(type)

                quality = kwargs['Quality'] if 'Quality' in kwargs else None
                if quality:
                    quality_min, quality_max = self.parse_lvls_from_str(quality)

                    if quality_min > 9 or quality_min < 1 or quality_max < 1 or quality_max > 9:
                        raise ValueError("sneakers lvls must be between 1 and 9")
                    if quality_min > quality_max:
                        raise ValueError("min sneakers lvls value > max sneakers lvls value")
                    self.api_url_obj.set_gems_quality(quality_min, quality_max)

            elif section == 'Others':
                if section not in self.pages:
                    raise ValueError(f"Invalid page: {section}")
                self.api_url_obj.set_page(section)

                quality = kwargs['Quality'] if 'Quality' in kwargs else None
                if quality:
                    if quality not in self.qualities:
                        raise ValueError('Unknown quality')
                    self.api_url_obj.set_quality(quality)

    @property
    def api_url(self):
        return self.api_url_obj.result_url

    def get_sneakers_from_pages(self, sessionID):
        url = self.api_url + f'&sessionID={sessionID}'
        api_content = requests.get(url).content
        all_sneakers = json.loads(api_content)['data']

        for i in range(1, 4):
            api_content = requests.get(url.replace('refresh=false&page=0', f'refresh=true&page={i}')).content
            all_sneakers.extend(json.loads(api_content)['data'])

        return all_sneakers

    def find_sneakers_by_otd(self, otd, sessionID):
        for sneaker in self.get_sneakers_from_pages(sessionID):
            if sneaker['otd'] == otd:
                return sneaker['id'], sneaker['sellPrice']


class ApiUrl():
    def __init__(self):
        self.chain = ''
        self.otd = ''
        self.type = ''
        self.gtype = ''
        self.quality = ''
        self.level = '0'
        self.bread = '0'

    def set_all_type(self, val):
        if val == 'Sneakers':
            self.type = 600
        if val == 'Shoeboxes':
            self.type = 301

    def set_sneakers_rarity(self, val):
        if val == 'OG':
            self.otd = 2
        if val == 'Genesis':
            self.otd = 1

    def set_quality(self, val):
        if val == 'Common':
            self.quality = 1
        if val == 'Uncommon':
            self.quality = 2
        if val == 'Rare':
            self.quality = 3
        if val == 'Epic':
            self.quality = 4
        if val == 'Legendary':
            self.quality = 5

    def set_sneakers_class(self, val):
        if val == 'Walker':
            self.type = 601
        if val == 'Jogger':
            self.type = 602
        if val == 'Runner':
            self.type = 603
        if val == 'Trainer':
            self.type = 604

    def set_page(self, val):
        if val == 'Gems':
            self.type = 501
        if val == 'Others':
            self.type = 701

    def set_gems_type(self, val):
        if val == 'Efficiency':
            self.gtype = 1
        if val == 'Luck':
            self.gtype = 2
        if val == 'Comfort':
            self.gtype = 3
        if val == 'Resilience':
            self.gtype = 4

    def set_sneakers_lvl(self, val_min, val_max):
        if val_max < 9:
            val_max = f'0{val_max + 1}'
        else:
            val_max += 1
        val_min += 1
        self.level = f'{val_min}0{val_max}'

    def set_sneakers_shoe_mint(self, val_min, val_max):
        if val_max < 9:
            val_max = f'0{val_max + 1}'
        else:
            val_max += 1
        val_min += 1
        self.bread = f'{val_min}0{val_max}'

    def set_gems_quality(self, val_min, val_max):
        if val_max < 9:
            val_max = f'0{val_max + 1}'
        else:
            val_max += 1
        val_min += 1
        self.level = f'{val_min}0{val_max}'

    def set_chain(self, val):
        if val in ['SOL', 'sol']:
            self.chain = 103
        if val in ['BNB', 'bnb']:
            self.chain = 104
        if val in ['ETH', 'eth']:
            self.chain = 101

    @property
    def result_url(self):
        return f'https://api.stepn.com/run/orderlist?order=2001&chain={self.chain}&refresh=false&page=0&otd={self.otd}&type={self.type}&gType={self.gtype}&quality={self.quality}&level={self.level}&bread={self.bread}'
