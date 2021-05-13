import requests
from bs4 import BeautifulSoup

class Opinion:
    def __init__(self, content):
        self.id = content["data-entry-id"]
        
        self.author = content.select("span.user-post__author-name")[0].text
        
        try:
            temp = content.select("span.user-post__author-recomendation>em")[0].text
            if temp == "Polecam":
                self.recommended = True
            elif temp == "Nie polecam":
                self.recommended = False
        except IndexError:
            self.recommended = None
        
        self.rating = content.select("span.user-post__score-count")[0].text.split("/")[0]
        
        self.content = content.select("div.user-post__text")[0].text
        
        self.positives = []
        self.negatives = []
        columns = content.select("div.review-feature__col")
        for col in columns:
            if len(col.select("div.review-feature__title--negatives")) == 0:
                items = col.select("div.review-feature__item")
                for item in items:
                    self.positives.append(item.text)
            else:
                items = col.select("div.review-feature__item")
                for item in items:
                    self.negatives.append(item.text)
        
        self.upvoteCount = content.select("button.vote-yes")[0].select("span")[0].text
        self.downvoteCount = content.select("button.vote-no")[0].select("span")[0].text
        
        temp = content.select("time")
        self.publishDate = temp[0]["datetime"]
        if len(temp) == 2:
            self.purchaseDate = temp[1]["datetime"]
        else:
            self.purchaseDate = None
    def asJSON(self):
        return {
            'id':self.id,
            'author':self.author,
            'recommended':self.recommended,
            'rating':self.rating,
            'content':self.content,
            'positives':self.positives,
            'negatives':self.negatives,
            'helpful':self.upvoteCount,
            'unhelpful':self.downvoteCount,
            'publishDate':self.publishDate,
            'purchaseDate':self.purchaseDate
        }