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
            val_max = f'0{val_max+1}'
        else:
            val_max +=1
        val_min += 1
        self.level = f'{val_min}0{val_max}'

    def set_sneakers_shoe_mint(self, val_min, val_max):
        if val_max < 9:
            val_max = f'0{val_max+1}'
        else:
            val_max +=1
        val_min += 1
        self.bread = f'{val_min}0{val_max}'

    def set_gems_quality(self, val_min, val_max):
        if val_max < 9:
            val_max = f'0{val_max+1}'
        else:
            val_max +=1
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
        return f'https://api.stepn.com/run/orderlist?order=2001&chain={self.chain}&refresh=true&page=0&otd={self.otd}&type={self.type}&gType={self.gtype}&quality={self.quality}&level={self.level}&bread={self.bread}'
