# main.py
# Imports
import argparse
from rich import print
from date import advance_date, get_date, print_date
from inventory import display_sales, display_purchases, display_inventory, get_sold_items, get_bought_items
from sell import sell_item
from buy import buy_item
from metrics import calculate_total_cost, calculate_total_revenue, calculate_total_profit, calculate_revenue_by_date, calculate_revenue_between_dates, calculate_cost_by_date, calculate_profit_between_dates, get_sold_items, write_profit_to_file, write_cost_to_file, write_revenue_to_file


# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.
parser = argparse.ArgumentParser(description="Supermarket Supply Administer")
subparsers = parser.add_subparsers(dest="command", required=True)

# dateparsers
advance_date_parser = subparsers.add_parser(
    "advancedate", help="Advance the date by the number of days")
advance_date_parser.add_argument(
    'days', type=int, help="Number of days to advance")
advance_date_parser.set_defaults(func=advance_date)

today_parser = subparsers.add_parser('today', help="Show the current date")
today_parser.set_defaults(func=get_date)

# totalcost parser
totalcost_parser = subparsers.add_parser(
    'totalcost', help="Calculate total cost of all items bought")
totalcost_parser.set_defaults(func=calculate_total_cost)

# revenueparsers
totalrevenue_parser = subparsers.add_parser(
    'totalrevenue', help="Calculate total revenue from sales")
totalrevenue_parser.set_defaults(func=calculate_total_revenue)

# totalprofit parser
totalprofit_parser = subparsers.add_parser(
    'totalprofit', help="Calculate total profit (total revenue - total cost)")
totalprofit_parser.set_defaults(func=calculate_total_profit)


# datecost parser
datecost_parser = subparsers.add_parser(
    'datecost', help="Calculate total cost for a specific date or date range")
datecost_parser.add_argument(
    'start_date', help="Start date (YYYY-MM-DD)")
datecost_parser.add_argument(
    'end_date', nargs='?', help="End date (YYYY-MM-DD)")
datecost_parser.set_defaults(func=calculate_cost_by_date)


# daterevenue parser
date_revenue_parser = subparsers.add_parser(
    'daterevenue', help="Display revenue between dates")
date_revenue_parser.add_argument(
    'start_date', nargs='?', help="Start date (YYYY-MM-DD)")
date_revenue_parser.add_argument(
    'end_date', nargs='?', help="End date (YYYY-MM-DD)")
date_revenue_parser.set_defaults(func=calculate_revenue_between_dates)

# dateprofit parser
dateprofit_parser = subparsers.add_parser(
    'dateprofit', help="Calculate total profit for a specific date or date range")
dateprofit_parser.add_argument(
    'start_date', help="Start date (YYYY-MM-DD) to calculate total profit")
dateprofit_parser.add_argument(
    'end_date', nargs='?', help="End date (YYYY-MM-DD) to calculate total profit")
dateprofit_parser.set_defaults(func=calculate_profit_between_dates)


# buyparsers
buy_parser = subparsers.add_parser(
    'buy', help="Register a purchase of a product")
buy_parser.set_defaults(func=buy_item)

# sellparsers
sell_parser = subparsers.add_parser(
    'sell', help="Register a sale of a product")
sell_parser.set_defaults(func=sell_item)

# inventoryparsers
inventory_parser = subparsers.add_parser(
    'inventory', help="Display the current inventory")
inventory_parser.set_defaults(func=display_inventory)


# sales_historyparser
sales_parser = subparsers.add_parser('sales', help="Display sales history")
sales_parser.set_defaults(func=display_sales)

# purchase_historyparser
purchases_parser = subparsers.add_parser(
    'purchases', help="Display purchase history")
purchases_parser.set_defaults(func=display_purchases)

# Parse the command-line arguments
args = parser.parse_args()


def main():

    sales_data = [
        {"date": "2023-01-01", "price": 10.0, "quantity": 5},
        {"date": "2023-01-02", "price": 15.0, "quantity": 3},
    ]
    sold_items = get_sold_items()
    bought_items = get_bought_items()

    if args.command == "today":
        print_date()
    elif args.command == "advancedate":
        if args.days is not None:
            advance_date(args.days)
        else:
            print("Please provide the number of days to advance.")
    elif args.command == "sales":
        display_sales()
    elif args.command == "inventory":
        display_inventory()
    elif args.command == "sell":
        sell_item()
    elif args.command == "totalcost":
        total_cost = calculate_total_cost()
        if total_cost is not None:
            print(f"Total cost of all items bought: ${total_cost:.2f}")
        else:
            print("Error calculating total cost.")
    elif args.command == "totalrevenue":
        total_revenue = calculate_total_revenue()
        if total_revenue is not None:
            print(f"Total revenue from sales: ${total_revenue:.2f}")
        else:
            print("Error calculating total revenue.")
    elif args.command == "totalprofit":
        total_profit = calculate_total_profit()
        if total_profit is not None:
            print(f"Total profit: ${total_profit:.2f}")
        else:
            print("Error calculating total profit.")
    elif args.command == "purchases":
        display_purchases()
    elif args.command == "datecost":
        if args.start_date:
            total_cost = calculate_cost_by_date(args.start_date, args.end_date)
            write_cost_to_file(args.start_date, args.end_date, total_cost)
        else:
            print("Invalid command. Please provide a start_date.")

    elif args.command == "daterevenue":
        if args.start_date:
            if args.end_date:
                total_revenue = calculate_revenue_between_dates(
                    args.start_date, args.end_date)
            else:
                total_revenue = calculate_revenue_by_date(args.start_date)
            write_revenue_to_file(
                args.start_date, args.end_date, total_revenue)
        else:
            print("Invalid command. Please provide a start_date.")

    elif args.command == "dateprofit":
        if args.start_date:
            start_date = args.start_date
            end_date = args.end_date
            total_profit = calculate_profit_between_dates(start_date, end_date)
            write_profit_to_file(start_date, end_date, total_profit)
        else:
            print("Invalid command. Please provide a start_date.")
    elif args.command == "buy":
        buy_item()

    else:
        print("Invalid command. Please choose a valid command: today, advancedate, sales, inventory, sell, purchases, buy, totalcost")


if __name__ == "__main__":
    main()
