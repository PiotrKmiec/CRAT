from flask import Flask, render_template, request, redirect
from os import listdir
from os.path import isfile, join
from modules.product import Product
import json
from tinydb import TinyDB, Query

app = Flask(__name__, template_folder='templates')
db = TinyDB('data/tinyDB/products.json')


def getProductNames():
    IDs = []
    names = []

    for x in db:
        IDs.append(x["ID"])
        names.append(x["Name"])
    
    return [IDs, names]

@app.route("/")
def home():
    products = getProductNames()
    return render_template("index.html", products=products[0], names=products[1], amount=len(products[0]), errorID=request.args.get("err"))

@app.route("/extract/<var>")
def extract(var):
    print(var)

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
    return render_template("readProduct.html", opinions=item['Opinions'], title=item['Name'], id=item['ID'])

if __name__ == "__main__":
    app.run()

# create Author page, use jquery dataTables for opinion list (use own CSS)