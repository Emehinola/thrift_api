import datetime

from core.constants import MONTH_MAP_30, MONTH_MAP_31


class DateUtil:

    @staticmethod
    def get_date(index: int):

        today = datetime.date.today() + datetime.timedelta(days=30*index)

        month_addition = 0
        if today.day > 15: # more than 15 days into the month
            month_addition = 1 # start from next month
        
        if today.month == 12:
            month_addition = 0 # reset to january

        start_date = today.replace(day=1, month=today.month+month_addition)

        # check if next month has 30, 31 or 28 days
        if (today.month + 1 if today.day > 15 else today.month) in MONTH_MAP_30:
            end_date = today.replace(day=30, month=today.month+month_addition)
        elif (today.month + 1 if today.day > 15 else today.month) in MONTH_MAP_31:
            end_date = today.replace(day=31, month=today.month+month_addition)
        else:
            end_date = today.replace(day=28, month=today.month+month_addition) # february

        return start_date, end_date