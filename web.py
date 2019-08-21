from flask import Flask, render_template

from db import db, get_housemates, get_gas_total, get_internet_total, get_power_total, get_water_total, \
    get_total_owed, get_individual_unpaid_bills

app = Flask(__name__)


@app.route('/')
def index():
    housemates = get_housemates()
    total_owed = {}
    individual_bills = {}
    for housemate in housemates:
        owed = get_total_owed(housemate)
        if owed is not None:
            total_owed[housemate] = owed / 100
        else:
            total_owed[housemate] = 0

        individual_bills[housemate] = get_individual_unpaid_bills(housemate)

    gas_total = get_gas_total() / 100
    internet_total = get_internet_total() / 100
    power_total = get_power_total() / 100
    water_total = get_water_total() / 100

    return render_template("index.html", gas_total=gas_total, internet_total=internet_total, power_total=power_total,
                           water_total=water_total, housemates=housemates, total_owed=total_owed,
                           individual_bills=individual_bills)


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response
