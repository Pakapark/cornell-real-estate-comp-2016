from flask import Flask, render_template
from main import getRentRSF, getAllRentalIncome
import json
app = Flask(__name__)

@app.route('/')
def extractRentRSF():
    data, binaryMap = getRentRSF()
    totalRentalIncome = getAllRentalIncome(data, binaryMap)
    return render_template("index.html", result=json.dumps(data), binaryMap=json.dumps(binaryMap), totalRental = json.dumps(totalRentalIncome))
