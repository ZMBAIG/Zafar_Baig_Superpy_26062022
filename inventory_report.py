
import csv
from rich.console import Console
console = Console()
from rich import print
from rich.table import Table
from schedule_dates import to_get_datetime_object, to_get_change_day
from record_sell import to_get_purchased_items, to_get_purchased_ids

# This section gives a comprehensive report of the products with respect to Registered Number of items, Total Revenue, Total Number of sales, Total Number of Expired Items and Current Profit Gain/Loss on Total Stock. 

def to_get_existed_products(day):
    purchased_items         = to_get_purchased_items()
    purchased_ids           = to_get_purchased_ids()
    products_existence      = []
    for item in purchased_items:
        expire_date_object        = to_get_datetime_object(item["expiration_date"])
        purchase_date_object   = to_get_datetime_object(item["purchase_date"])
        if (
            item["product_id"] not in purchased_ids
            and purchase_date_object <= day
            and expire_date_object >= day
        ):
            products_existence.append(item)

    if len(products_existence)      == 0:
        console.print(f"\n[red on white blink]Item does not exist in inventory or sold out[/]\n")
    else:
        products_existence_sorted   = sorted(
            products_existence, key=lambda x: x["product_name"]
        )
        return products_existence_sorted

def stock_inventory(args):
    if args.now:
        day     =   to_get_change_day(0)
    if args.date:
        day     =   args.date[0].date()
    if args.yesterday:
        day     =   to_get_change_day(-1)
    products    =  to_get_existed_products(day)

    with open((f"stock_inventory_{day}.csv"), "w", newline="") as long_file:
        fieldnames = [
            "product_id",
            "product_name",
            "purchase_price",
            "amount",
            "purchase_date",
            "expiration_date",
        ]
        csv_writer = csv.DictWriter(long_file, fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(products)
        
# To present a data for visualization a table format is selected. In this form different style color of text is selected from a rich library.        

    table = Table(title=f"\nSUPERMARKET SUPERPY INVENTORY REPORT ({day})", show_lines=True)

    table.add_column("Product ID",          justify ="right",    style  = "bold blue on yellow")
    table.add_column("Product Name",                             style  ="bold red on white")
    table.add_column("Purchase Price €",    justify ="right",    style  = "bold red on blue")
    table.add_column("Amount",              justify ="right",    style  ="bold black on white")
    table.add_column("Purchase Date",       justify ="center",   style  ="bold white on green")
    table.add_column("Expiration Date",     justify ="center",   style  ="bold white on red")

    for item in products:
        table.add_row(
            item["product_id"],
            item["product_name"],
            item["purchase_price"],
            item["amount"],
            item["purchase_date"],
            item["expiration_date"],
        )

    console = Console(record=True)
    console.print(table)

    if args.txt:
        console.save_text(f"stock_inventory_{day}.txt")
