from datetime import datetime

from models import Bill
from power import decrypt_power_pdf, process_power_bill_email, process_power_bill_pdf
from utils import get_config, get_fetch_email


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


def main():
    water_bill = Bill(start_date=datetime(year=2019, month=6, day=24),
                      end_date=datetime(year=2019, month=7, day=23),
                      category="water",
                      total=107.30)

    summarize_bills([water_bill])

    start_fourway_split = datetime(year=2019, month=6, day=24)
    end_fourway_split = datetime(year=2019, month=7, day=6)
    water_fourway_split = split_bill(water_bill, start_fourway_split, end_fourway_split, 4)
    print("Water bill owed per person, split four ways: ${}".format(water_fourway_split))

    start_threeway_split = datetime(year=2019, month=7, day=6)
    water_threeway_split = split_bill(water_bill, start_threeway_split, water_bill.end_date, 3)
    print("Water bill owed per person, split three ways: ${}".format(water_threeway_split))

    print(water_threeway_split + water_fourway_split)

    # Get the power bill
    config = get_config()
    fetch = get_fetch_email(config)
    encrypted_bill = process_power_bill_email(fetch)
    decrypted_bill = decrypt_power_pdf(encrypted_bill)
    amt_due, service_start, service_end = process_power_bill_pdf(decrypted_bill)

    print("Amount due: ${}".format(amt_due))
    print("Service start: {}".format(service_start))
    print("Service end: {}".format(service_end))


if __name__ == "__main__":
    main()
