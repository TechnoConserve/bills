from datetime import datetime


def get_cost_per_day(cost, period):
    return cost / period.days


def split_cost_by_days(total_cost, num_days):
    return total_cost / num_days


class Bill:
    def __init__(self):
        self.water_start = None
        self.water_end = None
        self.service_period = None
        self.water_total = None
        self.water_per_day = None

    def water_bill(self):
        self.water_start = datetime(year=2019, month=6, day=24)
        self.water_end = datetime(year=2019, month=7, day=23)
        self.service_period = self.water_end - self.water_start

        self.water_total = 107.30
        self.water_per_day = get_cost_per_day(self.water_total, self.service_period)
        return self.service_period


def main():
    bill = Bill()
    bill.water_bill()
    print("Water bill total: ${}".format(bill.water_total))
    print("Water bill per day: ${}".format(bill.water_per_day))

    start_fourway_split = datetime(year=2019, month=6, day=24)
    end_fourway_split = datetime(year=2019, month=7, day=6)
    fourway_split_duration = end_fourway_split - start_fourway_split
    water_fourway_split = (bill.water_per_day * fourway_split_duration.days) / 4
    print("Water bill owed per person, split four ways: ${}".format(water_fourway_split))

    start_threeway_split = datetime(year=2019, month=7, day=6)
    end_threeway_split = bill.water_end
    threeway_split_duration = end_threeway_split - start_threeway_split
    water_threeway_split = (bill.water_per_day * threeway_split_duration.days) / 3
    print("Water bill owed per person, split three ways: ${}".format(water_threeway_split))

    print(water_threeway_split + water_fourway_split)


if __name__ == "__main__":
    main()
