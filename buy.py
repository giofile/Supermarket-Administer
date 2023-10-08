# buy.py
import csv
from datetime import datetime, timedelta
import os
from rich import print
from inventory import get_inventory, update_inventory

bought_link = './files/bought.csv'
inventory_link = './files/inventory.csv'
total_cost_file = './files/total_cost.txt'

headers = ['id', 'amount', 'product_name',
           'purchase_date', 'price', 'expiration_date', 'total_cost']


# Ensures the existence of the CSV file header, creating one if it doesn't exist, ensuring proper structure for data storage.
def create_csv_header():
    if not os.path.exists(bought_link) or os.path.getsize(bought_link) == 0:
        with open(bought_link, 'w', newline='') as file:
            writer = csv.writer(file, delimiter='|')
            writer.writerow(headers)


# This function reads the existing CSV file, extracts the last used ID, and ensures the new ID is unique for the next item. It handles file I/O intricacies and guarantees the integrity of item IDs, making it a complex operation.-->
def get_new_id(file_path):
    if not os.path.exists(file_path):
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


# Computes the expiration date based on the current date and a specified number of days, ensuring consistency in date format for items.
def get_expiration_date(days):
    today = datetime.today()
    new_date = today + timedelta(days=days)
    return new_date.strftime('%Y-%m-%d')


#  Retrieves the total cost value from a file, handling potential file not found or invalid data errors, and returning the total cost.
def get_total_cost():
    try:
        with open(total_cost_file, 'r') as cost_file:
            total_cost = float(cost_file.readline().strip())
    except (FileNotFoundError, ValueError):
        total_cost = 0.0

    return total_cost


# This function manages the updating of the total cost value in a file, ensuring accurate financial data. It handles file operations and data consistency, making it crucial for maintaining financial records and calculations within the inventory system-->
def update_total_cost(total_cost):
    try:
        with open(total_cost_file, 'w') as cost_file:
            cost_file.write(str(total_cost))
    except Exception as e:
        print(f"Error updating total cost: {str(e)}")


# This interactive function collects user inputs, validates them, performs calculations, and updates both financial records and the inventory system. It requires meticulous error handling, ensuring data integrity, and synchronization of actions, making it a complex and vital part of the purchasing process-->
def buy_item():
    product_name = input('Product: ')
    while True:
        try:
            amount = int(input('Amount of items bought: '))
            break
        except ValueError:
            print('Please try again with a whole number, example: 5')
    while True:
        try:
            buy_price = float(input('Amount paid (example input: 1.25): '))
            break
        except ValueError:
            print('Please try again with the correct format, example: 1.25')
    while True:
        try:
            expiration_days = int(
                input('Expiration date (days from now): '))
            break
        except ValueError:
            print('Please try again and enter the number of days, example: 5')

    total_cost = round(amount * buy_price, 2)
    current_total_cost = get_total_cost()
    updated_total_cost = current_total_cost + total_cost
    update_total_cost(updated_total_cost)
    expiration = get_expiration_date(expiration_days)
    create_csv_header()
    id = get_new_id(bought_link)
    today = datetime.today().strftime('%Y-%m-%d')
    with open(bought_link, 'a', newline='') as file:
        csv_writer = csv.writer(file, delimiter='|')
        csv_writer.writerow(
            [id, amount, product_name, today, buy_price, expiration, total_cost])

    formatted_text = f"You have purchased [bold light_green]{amount}[/bold light_green] {product_name} at a cost price of [bold light_green]${buy_price:.2f}[/bold light_green] each. They will expire on [bold light_green]{expiration}[/bold light_green]. Total Cost = [bold light_green]${amount * buy_price:.2f}[/bold light_green]"
    print(formatted_text)

    inventory = get_inventory()
    if product_name in inventory:
        inventory[product_name] += amount
    else:
        inventory[product_name] = amount

    update_inventory(inventory)


if __name__ == '__main__':
    buy_item()
