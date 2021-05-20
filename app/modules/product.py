import requests, json, os, sys
from bs4 import BeautifulSoup
import requests
from modules.opinion import Opinion
from utils import extractElement

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

class Product:
    def __init__(self, ID):
        self.ID = ID
        self.opinionList = []

        content = requests.get("https://www.ceneo.pl/"+ID+"#tab=reviews_scroll", auth=('user', 'pass'))
        soup = BeautifulSoup(content.text, 'html.parser')
        reviews = soup.select("div.js_product-review")

        self.title = soup.select("h1.js_product-h1-link")[0].contents[0]
        for review in reviews:
            self.opinionList.append(Opinion(review))

        while len(soup.select("a.pagination__next")) != 0:
            url = soup.select("a.pagination__next")[0]['href']
            
            content = requests.get("https://www.ceneo.pl/"+url, auth=('user', 'pass'))
            soup = BeautifulSoup(content.text, "html.parser")
            
            reviews = soup.select("div.js_product-review")
            
            for review in reviews:
                self.opinionList.append(Opinion(review))

    def toJSON(self):
        temp = []

        for x in range(0, len(self.opinionList)):
            temp.append(self.opinionList[x].__dict__())

        data = { "ID":self.ID,"Name":self.title,"Opinions":temp }

        with open('data/'+self.ID+'.json', 'w+') as file:
            json.dump(data, file)
            