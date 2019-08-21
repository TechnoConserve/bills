from flask import Flask, render_template

from db import db, get_housemates, get_gas_total, get_internet_total, get_power_total, get_water_total

app = Flask(__name__)


@app.route('/')
def index():
    housemates = get_housemates()
    gas_total = get_gas_total() / 100
    internet_total = get_internet_total() / 100
    power_total = get_power_total() / 100
    water_total = get_water_total() / 100

    return render_template("index.html", gas_total=gas_total, internet_total=internet_total, power_total=power_total,
                           water_total=water_total, housemates=housemates)


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response
