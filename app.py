from flask import Flask, render_template
from main import getRentRSF
import json
app = Flask(__name__)

@app.route('/')
def extractRentRSF():
    data, binaryMap = getRentRSF()
    return render_template("index.html", result=json.dumps(data), binaryMap=json.dumps(binaryMap))
