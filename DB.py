import json
import os

import mysql.connector
import yaml
from yaml import CLoader as Loader

with open(os.path.join(os.path.dirname(__file__), 'config.yaml'), 'r') as f:
    config = yaml.load(f, Loader=Loader)['DB']

class DB():
    def __init__(self):
        self.cnx = mysql.connector.connect(**config)
        self.cursor = self.cnx.cursor()

    def get_filters(self, id: int) -> json:
        self.cursor.execute(
            'SELECT filters FROM projects WHERE id=%s', (id,)
        )
        data = self.cursor.fetchall()
        self.cnx.commit()
        print(data[0][0])

        return json.loads(data[0][0])

    def __del__(self):
        self.cnx.close()