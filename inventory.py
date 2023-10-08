# inventory.py
import csv
import os
from date import get_date
from rich.console import Console
from rich.table import Table
import json

purchases_link = './files/purchases.csv'
bought_link = './files/bought.csv'
sold_link = './files/sold.csv'
inventory_link = './files/inventory.csv'
json_inventory = './files/inventory.json'
json_sales = './files/sales.json'
json_purchases = './files/purchases.json'

console = Console()


# Loads or creates a JSON file with given default value.
def load_or_create_json(file_path, default_value=None):
    if os.path.exists(file_path):
        with open(file_path, 'r') as jsonfile:
            try:
                data = json.load(jsonfile)
            except json.JSONDecodeError:
                data = default_value
    else:
        if default_value is not None:
            with open(file_path, 'w') as jsonfile:
                json.dump(default_value, jsonfile, indent=4)
            data = default_value
        else:
            data = []

    return data


# Checks if a file exists at the given file path.
def file_exists(file_path):
    return os.path.isfile(file_path)


# This function searches for a specific item in the list of bought items, necessitating knowledge of dictionary manipulation and iteration. It enables the identification of unique items based on their name and quantity, providing a key reference for other parts of the system.-->
def get_bought_id(product_name, amount):
    bought_items = get_bought_items()
    for item in bought_items:
        if item['product_name'] == product_name and int(item['amount']) == amount:
            return item['id']
    return None


# This function retrieves a list of bought items from a CSV file, requiring an understanding of file I/O operations and CSV parsing. It organizes the data into a list of dictionaries, providing a foundation for other functions that depend on this initial data retrieval.--->
def get_bought_items():
    bought_items = []
    try:
        if file_exists(bought_link):
            with open(bought_link, 'r', encoding='utf-8-sig') as bought_object:
                reader = csv.DictReader(bought_object, delimiter='|')
                for row in reader:
                    bought_items.append(row)
        else:
            print(f"File not found: {bought_link}")
    except Exception as e:
        print(f"Error reading {bought_link}: {str(e)}")
    return bought_items


# Retrieves a list of sold item IDs from the 'sold.csv' file.
def get_sold_ids():
    sold_ids = []
    try:
        if file_exists(sold_link):
            with open(sold_link, 'r', encoding='utf-8-sig') as sold_object:
                reader = csv.DictReader(sold_object)
                for row in reader:
                    sold_ids.append(row['bought_id'])
        else:
            print(f"File not found: {sold_link}")
    except Exception as e:
        print(f"Error reading {sold_link}: {str(e)}")
    return sold_ids


# Retrieves a list of sold items from the 'sold.csv' file.
def get_sold_items():
    sold_items = []
    with open(sold_link, 'r', encoding='utf-8-sig') as sold_object:
        reader = csv.DictReader(sold_object, delimiter='|')
        for row in reader:
            sold_items.append(row)
    return sold_items


# This function identifies products that have expired based on their expiration date and whether they have been sold, showcasing conditional logic and date comparison. It plays a crucial role in managing inventory by ensuring expired items are properly tracked and managed.-->
def get_expired_products():
    bought_items = get_bought_items()
    sold_ids = get_sold_ids()
    expired_products = []
    today = get_date()
    for item in bought_items:
        if item['id'] not in sold_ids and item['expiration_date'] < today:
            expired_products.append(item)
    return expired_products


# Retrieves a list of sold items between specified dates from the 'sold.csv' file.
def get_sold_between_dates(first_date, second_date):
    sold_items = get_sold_items()
    items = []
    for item in sold_items:
        if item['sell_date'] >= first_date and item['sell_date'] <= second_date:
            items.append(item)
    return items


# Retrieves the current inventory from the 'inventory.csv' file.
def get_inventory():
    inventory = {}
    if os.path.exists(inventory_link):
        with open(inventory_link, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            for row in reader:
                product = row['Product']
                stock = int(row['Current stock'])
                inventory[product] = stock
    return inventory


# This function updates the inventory by decreasing the stock of a specific product, involving dictionary manipulation and conditional statements. It ensures accurate tracking of product quantities after sales, requiring an understanding of data structures and control flow.-->
def decrease_inventory(product_name, sold_amount):
    inventory = get_inventory()

    if product_name not in inventory:
        console.print(f"Error: {product_name} not found in inventory.")
        return

    current_stock = inventory[product_name]

    if current_stock >= sold_amount:
        inventory[product_name] -= sold_amount
        console.print(f"Inventory updated: {product_name} -{sold_amount}")
        update_inventory(inventory)
    else:
        console.print(
            f"Error: Not enough stock for {product_name} to sell {sold_amount}")

    return inventory


# This function displays the current inventory in a well-organized table format, enhancing user experience through structured data presentation.
def display_inventory():
    inventory = {}
    if os.path.exists(inventory_link):
        with open(inventory_link, 'r', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile, delimiter='|')
            for row in reader:
                product = row['Product']
                stock = int(row['Current stock'])
                inventory[product] = stock

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column('Product', style='dim', width=12)
    table.add_column('Current stock')

    for product, stock in inventory.items():
        table.add_row(product, str(stock))
    console.print(table)


# Updates the 'inventory.csv' and 'inventory.json' files with the updated inventory data.
def update_inventory(inventory):
    with open(inventory_link, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Product', 'Current stock']
        writer = csv.DictWriter(
            csvfile, fieldnames=fieldnames, delimiter='|')
        writer.writeheader()
        for product, stock in inventory.items():
            writer.writerow({'Product': product, 'Current stock': stock})

    with open(json_inventory, 'w') as jsonfile:
        json.dump(inventory, jsonfile)


# Displays the list of sold items using a formatted table.
def display_sales():
    sales = get_sold_items()

    table = Table(show_header=True, header_style="bold magenta")
    table.add_column('ID', style='dim', width=4)
    table.add_column('Product', style='dim', width=12)
    table.add_column('Amount')
    table.add_column('Date of sale', style='dim', width=15)
    table.add_column('Price')
    table.add_column('Total Earnings', style='dim', width=15)

    for item in sales:
        id_value = item['id']
        product_name = item['product_name']
        amount = item['amount']
        sell_date = item['sell_date']
        price = item['price']
        total_earnings = item['total_earnings']

        table.add_row(id_value, product_name, amount,
                      sell_date, price, total_earnings)

    console.print(table)

    with open(json_sales, 'w') as jsonfile:
        json.dump(sales, jsonfile, indent=4)


# Displays the list of purchased items using a formatted table and updates 'purchases.csv' and 'purchases.json' files.
def display_purchases():
    bought_items = get_bought_items()
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column('ID', style='dim', width=4)
    table.add_column('Amount', style='dim', width=8)
    table.add_column('Product', style='dim', width=8)
    table.add_column('Date of purchase', style='dim', width=13)
    table.add_column('Price', style='dim', width=8)
    table.add_column('Expiration date', style='dim', width=13)
    table.add_column('Total Cost', style='dim', width=8)

    for item in bought_items:
        id_value = item['id']
        amount = item['amount']
        product_name = item['product_name']
        purchase_date = item['purchase_date']
        price = item['price']
        expiration_date = item['expiration_date']
        total_cost = item['total_cost']

        table.add_row(id_value, amount, product_name,
                      purchase_date, price, expiration_date, total_cost)

    with open(purchases_link, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['ID', 'Amount', 'Product', 'Date of purchase',
                      'Price', 'Expiration date', 'Total Cost']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter='|')

        writer.writeheader()

        for item in bought_items:
            writer.writerow({
                'ID': item['id'],
                'Amount': item['amount'],
                'Product': item['product_name'],
                'Date of purchase': item['purchase_date'],
                'Price': item['price'],
                'Expiration date': item['expiration_date'],
                'Total Cost': item['total_cost']
            })

    with open(json_purchases, 'w') as jsonfile:
        json.dump(bought_items, jsonfile, indent=4)

    console.print(table)
