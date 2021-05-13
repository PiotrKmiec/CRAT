import requests
from bs4 import BeautifulSoup
from opinion import Opinion
import json

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
    def asJSON(self):
        return {
            "ID":self.ID,
            "Name":self.title,
            "Opinions":self.opinionList
        }
    def saveJSON(self):
        with open('./data/'+self.ID+'.json','w+') as outfile:
            json.dump(self.asJSON(), outfile)

                
temp = Product("97065427")
print("Opinions: "+str(len(temp.opinionList)))
temp.saveJSON()
            