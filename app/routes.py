from flask import Flask, redirect, url_for, render_template, request
import pandas, json
from os import listdir
from os.path import isfile, join

extractedProducts = [f for f in listdir("data") if isfile(join("data", f))]
for x in range(0, len(extractedProducts)):
    extractedProducts[x] = extractedProducts[x][:-5]


app = Flask(__name__, template_folder='templates')

@app.route("/")
def home():
    return render_template("index.html", products=extractedProducts)

@app.route("/extract")
def extract():
    return 0

if __name__ == "__main__":
    app.run()