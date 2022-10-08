from ApiUrl import ApiUrl
from DB import DB

def parse_lvls_from_str(string: str) -> tuple[int, int]:
    string = string.split('-')
    lvls = []
    for i in string:
        lvls.append(int(i.replace(' ', '')))
    return lvls[0], lvls[1]

class StepnApiUrl:
    def __init__(self, project_id):
        self.db = DB()
        filters = self.db.get_filters(project_id)
        self.sneakers_types = ['Sneakers', 'Shoeboxes']
        self.sneakers_rarities = ['Genesis', 'OG']
        self.qualities = ['Common', 'Uncommon', 'Rare', 'Epic', 'Legendary']
        self.sneakers_classes = ['Walker', 'Jogger', 'Runner', 'Trainer']
        self.pages = ['Gems', 'Others']
        self.gem_types = ['Efficiency', 'Luck', 'Comfort', 'Resilience']
        self.api_url_obj = ApiUrl()
        self.set_filters(list(filters)[0], **filters[list(filters)[0]])

    def set_filters(self, section: str, **kwargs) -> None:

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
                    lvl_min, lvl_max = parse_lvls_from_str(lvl)

                    if lvl_min > 30 or lvl_min < 0 or lvl_max < 0 or lvl_max > 30:
                        raise ValueError("sneakers lvls must be between 0 and 30")
                    if lvl_min > lvl_max:
                        raise ValueError("min sneakers lvls value > max sneakers lvls value")

                    self.api_url_obj.set_sneakers_lvl(lvl_min, lvl_max)

                shoe_mint = kwargs['Shoe mint'] if 'Shoe mint' in kwargs else None
                if shoe_mint:
                    shoe_min, shoe_max = parse_lvls_from_str(shoe_mint)

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
                    quality_min, quality_max = parse_lvls_from_str(quality)

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

q = StepnApiUrl(19)
print(q.api_url)