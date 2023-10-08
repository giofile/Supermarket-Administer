# sell.py
import csv
from datetime import datetime
from inventory import decrease_inventory, get_inventory, update_inventory
from rich import print
import os

sold_link = './files/sold.csv'
total_revenue_file = './files/total_revenue.txt'

headers = ['id', 'product_name', 'amount',
           'sell_date', 'price', 'total_earnings']


# Checks if a file exists at the specified path and returns True if it does, False otherwise.
def file_exists(file_path):
    return os.path.isfile(file_path)


# Creates the CSV file header with specified column names if the file does not exist.
def create_csv_header():
    if not file_exists(sold_link):
        with open(sold_link, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerow(headers)


# Generates a new unique ID for a record in the CSV file based on existing IDs.
def get_new_id(file_path):
    if not file_path:
        return 1
    with open(file_path, 'r') as file:
        lines = file.readlines()
        if not lines:
            return 1
        for line in reversed(lines):
            line = line.strip()
            if line and not line.startswith('id|'):
                last_id = int(line.split('|')[0])
                return last_id + 1
    return 1


# Reads and returns the total revenue from the 'total_revenue.txt' file, handling file not found or invalid data errors.
def get_total_revenue():
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


# Manages accurate revenue tracking by updating and storing total earnings in 'total_revenue.txt'.
def update_total_revenue(amount):
    try:
        total_revenue = get_total_revenue() + amount
        with open(total_revenue_file, 'w') as revenue_file:
            revenue_file.write(str(total_revenue))
    except Exception as e:
        print(f"Error updating total revenue: {str(e)}")


# Manages the process of selling items, handling user inputs for product name, amount, and price, updating sales data in 'sold.csv' and adjusting inventory accordingly, while also updating total revenue.
def sell_item():
    product_name = input('Product: ')
    inventory = get_inventory()  # Get the current inventory

    if product_name not in inventory:
        print(f"Error: {product_name} not found in inventory.")
        return

    available_stock = inventory[product_name]
    while True:
        try:
            amount = int(input('Amount sold: '))
            if available_stock >= amount:
                break
            else:
                print(
                    f"Error: Not enough stock for {product_name}. Available stock: {available_stock}")
        except ValueError:
            print('Please try again with a whole number, example: 5')

    while True:
        try:
            sell_price = float(
                input('Selling price per item (example input: 1.25): '))
            break
        except ValueError:
            print('Please try again with the correct format, example: 1.25')

    total_earnings = round(amount * sell_price, 2)

    create_csv_header()
    id = get_new_id(sold_link)
    today = datetime.today().strftime('%Y-%m-%d')
    with open(sold_link, 'a', newline='') as file:
        csv_writer = csv.writer(file, delimiter='|')
        csv_writer.writerow(
            [id, product_name, amount, today, sell_price, total_earnings])

    decrease_inventory(product_name, amount)

    formatted_text = f"You have sold [bold light_red]{amount}[/bold light_red] {product_name} at a selling price of [bold light_red]${sell_price:.2f}[/bold light_red] each. Total Earnings = [bold light_red]${total_earnings:.2f}[/bold light_red]"
    print(formatted_text)

    update_inventory(get_inventory())

    update_total_revenue(total_earnings)


if __name__ == '__main__':
    sell_item()
