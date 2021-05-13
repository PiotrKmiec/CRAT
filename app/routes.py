from flask import Flask, render_template, request
from os import listdir
from os.path import isfile, join
from modules.product import Product
import json

extractedProducts = [f for f in listdir("data") if isfile(join("data", f))]
for x in range(0, len(extractedProducts)):
    extractedProducts[x] = extractedProducts[x][:-5]

app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    
    return render_template("index.html", products=extractedProducts)

@app.route("/extract/<var>")
def extract(var):

    temp = Product(var)
    temp.toJSON()
    return temp.title

@app.route("/showOpinions")
def show():

    with open("data/"+request.args.get('product')+".json","r+") as file:
        data = json.load(file)

    return data['Name']

if __name__ == "__main__":
    app.run()