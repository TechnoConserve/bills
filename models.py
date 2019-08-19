from datetime import datetime


class Bill:
    def __init__(self, start_date, end_date, category, total):
        self.start_date = start_date
        self.end_date = end_date
        self.service_period = self.end_date - self.start_date
        self.category = category
        self.total = total
        self.cost_per_day = self.get_cost_per_day()

    def get_cost_per_day(self):
        return self.total / self.service_period.days

    def split_cost_by_days(self, num_days):
        return self.total / num_days
