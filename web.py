from flask import Flask, render_template

from db import categories, db, get_housemates, get_gas_total, get_internet_total, get_power_total, get_water_total, \
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

    # Get an individual bill of each category
    gas_bill = None
    internet_bill = None
    power_bill = None
    water_bill = None
    for housemate, ind_bill_lst in individual_bills.items():
        for bill in ind_bill_lst:
            if bill.category == categories[0][0]:
                gas_bill = bill
            elif bill.category == categories[1][0]:
                internet_bill = bill
            elif bill.category == categories[2][0]:
                power_bill = bill
            elif bill.category == categories[3][0]:
                water_bill = bill

        # Break the loop if we have an example of all categories
        if gas_bill is not None and internet_bill is not None and power_bill is not None and water_bill is not None:
            break

    gas_total = get_gas_total() / 100
    internet_total = get_internet_total() / 100
    power_total = get_power_total() / 100
    water_total = get_water_total() / 100

    return render_template("index.html", gas_total=gas_total, internet_total=internet_total, power_total=power_total,
                           water_total=water_total, housemates=housemates, total_owed=total_owed,
                           individual_bills=individual_bills, gas_bill=gas_bill, internet_bill=internet_bill,
                           power_bill=power_bill, water_bill=water_bill)


@app.before_request
def before_request():
    db.connect()


@app.after_request
def after_request(response):
    db.close()
    return response
