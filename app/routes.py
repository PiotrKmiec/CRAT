from flask import Flask, render_template, request, redirect
from os import listdir
from os.path import isfile, join
from modules.product import Product
import json

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    extractedProducts = [f for f in listdir("data") if isfile(join("data", f))]
    for x in range(0, len(extractedProducts)):
        extractedProducts[x] = extractedProducts[x][:-5]
    return render_template("index.html", products=extractedProducts, errorID=request.args.get("err"))

@app.route("/extract/<var>")
def extract(var):
    print(var)

    if not var.isdecimal():
        return redirect("/?err=2")
    if len(var)>9 or len(var)<8:
        return redirect("/?err=1")

    temp = Product(var)
    temp.toJSON()

    return redirect("/showOpinions?product="+var)

@app.route("/showOpinions")
def show():

    with open("data/"+request.args.get('product')+".json","r+") as file:
        data = json.load(file)

    return render_template("readProduct.html", opinions=data["Opinions"], title=data["Name"])

if __name__ == "__main__":
    app.run()