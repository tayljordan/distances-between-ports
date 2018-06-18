from os import listdir
from os.path import isfile, join
import json

class Ports(object):

    def __init__(self, base_path):

        self.mypath = join(base_path, 'distances_json')
        self.onlyfiles = [f for f in listdir(self.mypath) if isfile(join(self.mypath, f))]
        self.dist = []

        for item in self.onlyfiles:
            file_path = join(self.mypath, item)
            with open(file_path, encoding='utf-8') as data_file:
                data = json.loads(data_file.read())
                for item in data['Port distances']:
                    self.dist.append(item)

        self.jsonkeys = [k for k in self.dist[0].keys()]

        self.cities = []

        for num, item in enumerate(self.dist):
            self.cities.append(item['properties']['city'])
