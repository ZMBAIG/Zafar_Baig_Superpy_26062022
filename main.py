# Imports
import argparse
from datetime import datetime
import textwrap
from purchase_product import purchase_product
from schedule_dates import to_get_advance_time, to_get_current_date
from record_sell import to_get_sell_item
from inventory_report import stock_inventory
from expired_schedule import to_generate_expired_products
from generate_revenue import to_generate_revenue
from generate_profit import get_profit
from rich.console import Console
console = Console()
from rich import print
from rich.panel import Panel

# Do not change these lines.
__winc_id__ = "a2bc36ea784242e4989deb157d527ba0"
__human_name__ = "superpy"

# Your code below this line.
def main():

    def to_get_valid_date(date_str):
        try:
            return datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            msg = "Please enter a valid date: '{0}'.".format(date_str)
            raise argparse.ArgumentTypeError(msg)
        
    # The argparse module makes it easy to write user-friendly command-line interfaces. The program defines what arguments it requires, and argparse will figure out how to parse those out of sys.argv. The argparse module also automatically generates help and usage messages and issues errors when users give the program invalid arguments. So here we use argparse command line tools for supermarket inventory, like --product_id, --amount, --yesterday etc etc.    

    parser = argparse.ArgumentParser(
        console.print(Panel.fit("Welcome to the [blink bold dark_red underline2]:apple::apple::apple:Supermarket SuperPy.:apple::apple::apple:[/] This App is build on a [overline]Command-Line Tool[/] that the Supermarket SuperPy will use to keep track of their all the daily Stock's activities  in inventory.", style="bold blue on #d7ffff\n")),
        console.print(Panel.fit("\n[green]To access well-structured and user friendly command-line interface with clear descriptions of each argument in the --help section, please, explore from the HELP file. [yellow]e.g. python3 main.py -h[/]\n")),

        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
        """
        ==============================================================================================================================
            
                                        to_get_current_date   This is a real-time date. i.e Today: yyyy-mm-dd
                                        to_get_advance_time   Advance Time relates with 'today,tomorrow or yesterday' 
                                        purchase              Purchase a product, e.g. orange 0.8 2022-12-31
                                        sell                  Sell a product, e.g. orange 2.99
                                        stock_inventory       It shows stock inventory with product's information.
                                        expired               It indicates all the expired products until now.
                                        revenue               Comprehensive report over revenue collection.
                                        profit                Comprehensive report over profit collection.
                    
        ==============================================================================================================================
                \n
        """,
        ),
    )
    parser.set_defaults(func=None)

    subparsers = parser.add_subparsers(
        dest="subparser_name",
    )
    to_get_current_date_parser = subparsers.add_parser(
        "to_get_current_date",
        description="This will change the 'system'-date or reset date to real-time 'today'",
    )
    to_get_current_date_parser.add_argument(
        "date_now",
        help="This will change date to real-time or present date i.e. today",
        action="store_true",
    )
    to_get_current_date_parser.set_defaults(func=to_get_current_date)

    to_get_advance_time_parser = subparsers.add_parser(
        "to_get_advance_time",
        description="This will be used to select a dates in future or past with respect to current date.",
    )
    to_get_advance_time_parser.add_argument(
        "to_get_advance_time",
        help="Please enter the current date 'today' to a date in future or past: to_get_advance_time [number of days]",
        nargs=1,
        type=int,
    )
    to_get_advance_time_parser.set_defaults(func=to_get_advance_time)

    purchase_parser = subparsers.add_parser(
        "purchase",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
        purchasing product:
        Amount: default 1
        Syntax: purchase [product_name] [price] [expiration_date] --amount [number or items]
        """
        ),
    )
    purchase_parser.add_argument("product_name", nargs=1, help="The name of the product that is going to store in inventory")
    purchase_parser.add_argument("price", type=float, nargs=1, help="It includes purchase price")
    purchase_parser.add_argument(
        "expiration_date",
        type=to_get_valid_date,
        help="This will indicates expiration date of purchased product, i.e. in yyyy-mm-dd",
    )
    purchase_parser.add_argument(
        "--amount",
        type=int,
        default=1,
        help="Please enter quantity of the purchased product (default: 1)",
    )
    purchase_parser.set_defaults(func=purchase_product)

    sell_parser = subparsers.add_parser(
        "sell",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        description=textwrap.dedent(
            """
        Selling product:
        Amount: default 1 and maximum of 3
        Syntax: purchase [product_name] [price] --amount [number or items]
        """
        ),
    )
    sell_parser.add_argument("product_name", nargs=1, help="Please enter product name")
    sell_parser.add_argument(
        "sell_price", type=float, nargs=1, help="Please enter sell's price of an item"
    )
    sell_parser.add_argument(
        "--amount",
        type=int,
        default=1,
        choices=range(1, 4),
        help="Enter number of items to be registered,(default: 1) and maximum of 3",
    )
    sell_parser.set_defaults(func=to_get_sell_item)

    date_parent_parser = subparsers.add_parser("date", add_help=False)
    date_parent_parser.add_argument(
        "--now", action="store_true", help="Select date to 'today'"
    )
    date_parent_parser.add_argument(
        "--yesterday",
        action="store_true",
        help="Select date to yesterday",
    )
    date_parent_parser.add_argument(
        "--date",
        type=to_get_valid_date,
        nargs=1,
        help="Select desire date: yyyy-mm-dd",
    )

    stock_inventory_parser = subparsers.add_parser(
        "stock_inventory",
        parents=[date_parent_parser],
        description="Stock inventory with relevant product information.",
    )
    stock_inventory_parser.add_argument(
        "--txt", action="store_true", help="exports to txt.file"
    )
    stock_inventory_parser.set_defaults(func=stock_inventory)

    expired_parser = subparsers.add_parser(
        "expired", description="It will Show a number of expired products till 'today'"
    )
    expired_parser.add_argument(
        "--txt", action="store_true", help="It will create and exports to txt.file"
    )
    expired_parser.set_defaults(func=to_generate_expired_products)

    revenue_parser = subparsers.add_parser(
        "revenue",
        parents=[date_parent_parser],
        description="This will generate a revenue for specific date or period",
    )
    revenue_parser.add_argument(
        "--period",
        type=to_get_valid_date,
        nargs=2,
        help="Select a period of two different dates with format of : yyyy-mm-dd",
    )
    revenue_parser.set_defaults(func=to_generate_revenue)

    profit_parser = subparsers.add_parser(
        "profit",
        parents=[date_parent_parser],
        description="This will generate profit for date or period",
    )
    profit_parser.add_argument(
        "--period",
        type=to_get_valid_date,
        nargs=2,
        help=" Select a period of two different dates with format of : yyyy-mm-dd",
    )
    profit_parser.set_defaults(func=get_profit)

    args = parser.parse_args()

    if args.func:
        args.func(args)


if __name__ == "__main__":
    main()
