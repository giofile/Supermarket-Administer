# date.py
import datetime


def get_date():
    current_date = datetime.datetime.now().date()
    return current_date.strftime('%Y-%m-%d')


def print_date():
    current_date = get_date()
    print(f'The current system date is: {current_date}')


# This function allows users to advance the current date by the specified number of days. It validates the input to ensure it's a valid number, calculates the new date, and provides clear error messages, ensuring accurate date manipulations in the application.-->
def advance_date(days):
    try:
        days = int(days)
        today = datetime.datetime.now().date()
        new_date = today + datetime.timedelta(days=days)
        print(f'The new date is now {new_date}.')
    except ValueError:
        print('Error: Please try again and enter a valid number.')
