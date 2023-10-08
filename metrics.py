# Here you will find all the financial - analysis
# metrics.py
from inventory import get_bought_items, get_sold_items
from rich import print


total_cost_file = './files/total_cost.txt'
total_revenue_file = './files/total_revenue.txt'
cost_data = './files/cost.txt'
revenue_data = './files/revenue.txt'
profit_data = './files/profit.txt'


#  basic logic functions -->
def calculate_total_cost():
    try:
        with open(total_cost_file, 'r') as cost_file:
            return float(cost_file.readline().strip())
    except FileNotFoundError:
        print("Total cost file not found. Creating a new file.")
        with open(total_cost_file, 'w') as cost_file:
            cost_file.write("0.0")
        return 0.0
    except ValueError:
        print("Invalid total cost value in the file. Resetting total cost to 0.0.")
        with open(total_cost_file, 'w') as cost_file:
            cost_file.write("0.0")
        return 0.0


def calculate_total_revenue():
    try:
        with open(total_revenue_file, 'r') as revenue_file:
            total_revenue = revenue_file.readline().strip()
            if total_revenue:
                return float(total_revenue)
            else:
                return 0.0
    except (FileNotFoundError, ValueError):
        print("Error: Total revenue file not found or contains invalid data.")
        return 0.0


def calculate_total_profit():
    total_cost = calculate_total_cost()
    total_revenue = calculate_total_revenue()

    total_profit = total_revenue - total_cost
    return total_profit
# _____________________________________________________


# Computes total revenue on a specific date by iterating through sales data, identifying matching dates, and summing up earnings of sold items.
def calculate_revenue_by_date(target_date):
    sales_data = get_sold_items()
    total_revenue = 0

    for sale in sales_data:
        sale_date = sale.get('sell_date')
        amount = int(sale.get('amount'))
        earnings = float(sale.get('total_earnings'))

        if sale_date and sale_date == target_date:
            total_revenue += earnings

    return total_revenue


#  this one may not be used, but i spend hours and hours debugging, so i leave this "display revenue" code , also as a reference->
def display_revenue(sales_data, target_date):
    total_revenue = calculate_revenue_by_date(sales_data, target_date)
    date_label = f" for {target_date}"
    revenue_info = f"Total revenue{date_label}: ${total_revenue:.2f}"
    print(revenue_info)


# Writes total revenue information to a file for a specific date range.
def write_revenue_to_file(start_date, end_date, total_revenue):
    try:
        date_label = f" for {start_date}" if not end_date else f" between {start_date} and {end_date}"
        revenue_info = f"Total revenue{date_label}: ${total_revenue:.2f}"
        with open(revenue_data, 'a') as file:
            file.write(revenue_info + '\n')
        print(revenue_info)
    except Exception as e:
        print(f"An error occurred: {e}")


# Calculates total cost within a specified date range or on a specific date by summing the costs of items bought within that period.
def calculate_cost_by_date(start_date, end_date=None):
    bought_items = get_bought_items()

    if end_date:
        total_cost = sum(float(item['total_cost'])
                         for item in bought_items if start_date <= item['purchase_date'] <= end_date)
    else:
        total_cost = sum(float(item['total_cost'])
                         for item in bought_items if item['purchase_date'] == start_date)

    return total_cost


# Writes total cost information to a file for a specific date range
def write_cost_to_file(start_date, end_date, total_cost):
    date_label = f" for {start_date}" if not end_date else f" between {start_date} and {end_date}"
    cost_info = f"Total cost{date_label}: ${total_cost:.2f}"
    with open(cost_data, 'a') as file:
        file.write(cost_info + '\n')
    print(cost_info)


# Calculates total profit on a specific date by subtracting the total cost of items bought from the total revenue earned from sales on that date.
def calculate_profit_by_date(date):
    try:
        sold_items = get_sold_items()
        bought_items = get_bought_items()

        total_cost = sum(float(item['total_cost']) for item in bought_items
                         if item['expiration_date'] == date)
        total_revenue = sum(float(item['total_earnings']) for item in sold_items
                            if item['sell_date'] == date)

        total_profit = total_revenue - total_cost

        return total_profit
    except FileNotFoundError:
        print("File not found.")
        return 0.0


# Calculates total revenue between specified start and end dates by iterating through sold items' data.
def calculate_revenue_between_dates(start_date, end_date):
    sold_items = get_sold_items()
    total_revenue = 0
    for item in sold_items:
        sell_date = item.get('sell_date')
        if start_date <= sell_date <= end_date:
            total_revenue += float(item.get('total_earnings', 0))
    return total_revenue


# Determines total profit within a date range or on a specific date by subtracting total cost from total revenue, considering both items bought and items sold during that period.
def calculate_profit_between_dates(start_date, end_date=None):
    sold_items = get_sold_items()
    bought_items = get_bought_items()

    if end_date:
        total_revenue = sum(float(item.get('total_earnings', 0))
                            for item in sold_items if start_date <= item.get('sell_date', '') <= end_date)
        total_cost = sum(float(item['total_cost'])
                         for item in bought_items if start_date <= item['purchase_date'] <= end_date)
    else:
        total_revenue = sum(float(item.get('total_earnings', 0))
                            for item in sold_items if item.get('sell_date', '') == start_date)

        total_cost = sum(float(item['total_cost'])
                         for item in bought_items if item['purchase_date'] == start_date)

    total_profit = total_revenue - total_cost
    return total_profit


# Writes total profit information to a file for a specific date range.
def write_profit_to_file(start_date, end_date, total_profit):
    date_label = f" for {start_date}" if not end_date else f" between {start_date} and {end_date}"
    profit_info = f"Total profit{date_label}: ${total_profit:.2f}"
    with open(profit_data, 'a') as file:
        file.write(profit_info + '\n')
    print(profit_info)


if __name__ == "__main__":
    total_cost = calculate_total_cost()
    total_revenue = calculate_total_revenue()

    print(f"Total cost of all items bought: ${total_cost:.2f}")
    print(f"Total revenue from sales: ${total_revenue:.2f}")

    total_profit = calculate_total_profit()
    print(f"Total profit: ${total_profit:.2f}")
