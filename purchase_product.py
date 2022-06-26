from rich.console import Console
console = Console()
from rich import print
import csv
from schedule_dates import to_get_date_today

# This section belongs to registration of purchasing a product. It makes sure the right product is going to be entering manually, with relevant attributes e.g. Product Name, Buying Date, Price, Expiration Date etc .etc. In this way the command line tool helps and enhance to store all the attributes of inventory item.

def to_get_product_id(file):
    with open(file, "r") as csv_file:
        reader = csv.reader(csv_file)
        product_id = len(list(reader))
        return product_id

def purchase_product(args):
    with open("bought.csv", "a", newline="") as bought_file:
        fieldnames = [
            "product_id",
            "product_name",
            "purchase_price",
            "amount",
            "purchase_date",
            "expiration_date",
        ]
        csv_writer = csv.DictWriter(bought_file, fieldnames=fieldnames)
        for i in range(args.amount):
            csv_writer.writerow(
                {
                    "product_id": to_get_product_id("bought.csv") + i,
                    "product_name": args.product_name[0].lower(),
                    "purchase_price": args.price[0],
                    "amount": 1,
                    "purchase_date": to_get_date_today(),
                    "expiration_date": args.expiration_date.date(),
                }
            )
    console.print(f"\n[bold white on green]The Product [red]{args.product_name[0]}[/] with number of items [red]{args.amount}[/] purchased and registered im inventory.[/]\n")
