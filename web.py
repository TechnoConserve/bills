from flask import Flask, render_template

from db import db, get_housemates, get_gas_total, get_internet_total, get_power_total, get_water_total

app = Flask(__name__)


@app.route('/')
def index():
    housemates = get_housemates()
    gas_total = get_gas_total()
    internet_total = get_internet_total()
    power_total = get_power_total()
    water_total = get_water_total()

    return render_template("index.html", gas_total=gas_total, internet_total=internet_total, power_total=power_total,
                           water_total=water_total, housemates=housemates)


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response
