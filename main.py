from datetime import datetime

from db import categories, get_housemates, IndividualBill
from gas import process_gas_bill_email
from internet import get_internet_bill
from models import Bill
from power import decrypt_power_pdf, process_power_bill_email, process_power_bill_pdf
from utils import get_config, get_fetch_email, start_flask


def split_bill(bill, start_date, end_date, num_split):
    period = end_date - start_date
    return (bill.cost_per_day * period.days) / num_split


def summarize_bills(bills):
    for bill in bills:
        print("{}: {}/{} to {}/{} is ${:.2f} (${:.2f} per day)".format(
            bill.category.title(),
            bill.start_date.month,
            bill.start_date.day,
            bill.end_date.month,
            bill.end_date.day,
            bill.total,
            bill.cost_per_day
        ))


def split_bills_between_housemates(bills):
    housemates = get_housemates()
    for bill in bills:
        # Split the bill into equal parts between housemates
        split_cost = int((bill.total / len(housemates)) * 100)

        # Create an IndividualBill assigned to each housemate
        for housemate in housemates:
            if housemate.name == "Avery Uslaner":
                paid = True
            else:
                paid = False
            housemate_bill, created = IndividualBill.get_or_create(debtor=housemate,
                                                                   service_start=bill.start_date,
                                                                   service_end=bill.end_date,
                                                                   category=bill.category,
                                                                   total=split_cost,
                                                                   paid=paid)
            if created:
                housemate_bill.save()


def main():
    # Get the power bill
    config = get_config()
    fetch = get_fetch_email(config)
    encrypted_bill = process_power_bill_email(fetch)
    decrypted_bill = decrypt_power_pdf(encrypted_bill)
    pwr_amt_due, service_start, service_end = process_power_bill_pdf(decrypted_bill)

    power_bill = Bill(start_date=service_start, end_date=service_end, category=categories[2][0],
                      total=pwr_amt_due)

    # Get the gas amount
    gas_amt_due = process_gas_bill_email(fetch)

    gas_bill = Bill(start_date=datetime(year=2019, month=7, day=26),
                    end_date=datetime(year=2019, month=8, day=15),
                    category=categories[0][0],
                    total=gas_amt_due)

    # Manually construct the water bill
    water_bill = Bill(start_date=datetime(year=2019, month=6, day=24),
                      end_date=datetime(year=2019, month=7, day=23),
                      category=categories[3][0],
                      total=107.30)

    # Get the internet bill
    internet_bill = get_internet_bill(2019, 8)

    bills = [gas_bill, internet_bill, power_bill, water_bill]

    summarize_bills(bills)
    split_bills_between_housemates(bills)

    start_fourway_split = datetime(year=2019, month=6, day=24)
    end_fourway_split = datetime(year=2019, month=7, day=6)
    water_fourway_split = split_bill(water_bill, start_fourway_split, end_fourway_split, 4)
    print("Water bill owed per person, split four ways: ${:.2f}".format(water_fourway_split))

    start_threeway_split = datetime(year=2019, month=7, day=6)
    water_threeway_split = split_bill(water_bill, start_threeway_split, water_bill.end_date, 3)
    print("Water bill owed per person, split three ways: ${:.2f}".format(water_threeway_split))

    start_flask(config["FLASK"]["DEBUG"])


if __name__ == "__main__":
    main()
