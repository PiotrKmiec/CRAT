from flask import Flask, render_template, request, redirect
from os import listdir
from os.path import isfile, join
from modules.product import Product
import json
from tinydb import TinyDB, Query
import pandas as pd

app = Flask(__name__, template_folder='templates')
db = TinyDB('data/products.json')


def getProductNames():
    IDs = []
    names = []
    stats = []

    for x in db:
        IDs.append(x["ID"])
        names.append(x["Name"])
        stats.append([x["OpinionsCount"],x["MeanRating"],x["Cons"],x["Pros"]])
    
    return [IDs, names, stats]

@app.route("/")
def home():
    products = getProductNames()
    return render_template("index.html", products=products[0], names=products[1], stats=products[2], amount=len(products[0]), errorID=request.args.get("err"))

@app.route("/extract/<var>")
def extract(var):

    if not var.isdecimal():
        return redirect("/?err=2")
    if len(var)>9 or len(var)<8:
        return redirect("/?err=1")

    temp = Product(var)
    temp.toTinyDB()

    return redirect("/showOpinions?product="+var)

@app.route("/showOpinions")
def show():

    item = db.search(Query().ID == request.args.get('product'))[0]
    data = {
            'id':[],
            'author':[],
            'recommended':[],
            'rating':[],
            'content':[],
            'positives':[],
            'negatives':[],
            'helpful':[],
            'unhelpful':[],
            'publishDate':[],
            'purchaseDate':[]
        }

    temp = ['id','author','recommended','rating','content','positives','negatives','helpful','unhelpful','publishDate','purchaseDate']

    ratio = [0,0,0]

    for x in item['Opinions']:
        for y in temp:
            data[y].append(x[y])
        if len(x['negatives']) == len(x['positives']):
            ratio[2]+=1
        elif len(x['negatives']) < len(x['positives']):
            ratio[0]+=1
        else:
            ratio[1]+=1
        

    for x in range(0, len(data['id'])):
        data['author'][x] = data['author'][x][1:]

        positives = ""
        for y in data['positives'][x]:
            positives += y+"  ,  "
        data['positives'][x] = positives[:-5]

        negatives = ""
        for y in data['negatives'][x]:
            negatives += y+"  ,  "
        data['negatives'][x] = negatives[:-5]

    cT = pd.DataFrame(data, columns=temp)

    return render_template("readProduct.html", title=item['Name'], id=item['ID'], table=cT.to_html(table_id="opinionTable"), meanRating=item['MeanRating'], prosCount=item['Pros'], consCount=item['Cons'], opinionsCount=item['OpinionsCount'], ratio=ratio)

@app.route("/author")
def author():
    return render_template("author.html")

if __name__ == "__main__":
    app.run()

# return a json file of product, return error if wrong post data sent