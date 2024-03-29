import requests, json, os, sys
from bs4 import BeautifulSoup
import requests
from modules.opinion import Opinion
from utils import extractElement
from tinydb import TinyDB, Query

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
        
        self.opinionsCount = len(self.opinionList)
        self.consCount = 0
        self.prosCount = 0
        meanRating = 0

        for opinion in self.opinionList:
            self.consCount += len(opinion.negatives)
            self.prosCount += len(opinion.positives)
            meanRating += float(opinion.rating.replace(',','.'))
        
        self.meanRating=round(meanRating/self.opinionsCount, 2)

    
    def toTinyDB(self):

        temp = []
        for x in range(0, len(self.opinionList)):
            temp.append(self.opinionList[x].__dict__())

        db = TinyDB('data/products.json')
        if len(db.search(Query().ID == self.ID)) > 0:
            db.update({'Name': self.title, 'Opinions': temp}, Query().ID == self.ID)
        else:
            db.insert({'ID': self.ID, 'Name': self.title, 'Opinions': temp, 'OpinionsCount':self.opinionsCount, 'MeanRating':self.meanRating, "Cons":self.consCount, "Pros":self.prosCount})

            