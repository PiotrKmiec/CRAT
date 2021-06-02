from flask import Flask, render_template, request, redirect
from os import listdir
from os.path import isfile, join
from modules.product import Product
import json

app = Flask(__name__, template_folder='templates')

def getIDs():
    IDs = [f for f in listdir("data") if isfile(join("data", f))]

    for x in range(0, len(IDs)):
        IDs[x] = IDs[x][:-5]
    return IDs


def getProducts():
    productIDs = getIDs()
    products = []
    productNames = []

    for x in productIDs:
        products.append(Product(x, True))
    for x in products:
        productNames.append(x.title)

    return [productIDs, productNames, products]

@app.route("/")
def home():
    products = getProducts()
    print(products[1])
    return render_template("index.html", products=products[0], names=products[1], amount=len(products[0]), errorID=request.args.get("err"))

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

    product = Product(request.args.get('product'), True)

    return render_template("readProduct.html", opinions=product.opinionList, title=product.title, id=product.ID)

if __name__ == "__main__":
    app.run()

# create Author page, use jquery dataTables for opinion list (use own CSS)
# dies irae dies illa