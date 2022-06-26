import csv
from rich.console import Console
console = Console()
from rich import print
from rich.table import Table
from record_sell import to_get_purchased_items, to_get_purchased_ids
from schedule_dates import to_get_datetime_object, to_get_date_today

# To get a schedule of different dates for certain events like expire, a function is defined that helps to add or subtract number of days with respect to current date(today).

today = to_get_date_today()
def to_get_expired_products():
    purchased_items                 =   to_get_purchased_items()
    purchased_ids                   =   to_get_purchased_ids()
    expired_products                =   []
    today_date                      =   to_get_datetime_object(today)
    for item in purchased_items:
        expire_date_object          =   to_get_datetime_object(item["expiration_date"])
        purchase_date_object        =   to_get_datetime_object(item["purchase_date"])
        if (
            item["product_id"] not in purchased_ids
            and purchase_date_object <= today_date
            and expire_date_object < today_date
        ):
            expired_products.append(item)

    if len(expired_products)        == 0:
        console.print(f"\n[bold white on green]There is no indication of product wasted until[/] {today_date}!\n")
    else:
        expired_products_sorted     = sorted(
            expired_products, key=lambda x: x["expiration_date"]
        )
    return expired_products_sorted

def to_generate_expired_products(args):
    expired_products = to_get_expired_products()
    with open(f"Product_Expired_{today}.csv", "w", newline="") as exp_file:
        fieldnames = [
            "product_id",
            "product_name",
            "purchase_price",
            "amount",
            "purchase_date",
            "expiration_date",
        ]
        csv_writer = csv.DictWriter(exp_file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(expired_products)

    table = Table(title=f"EXPIRED ITEMS UNTIL {today}", show_lines=True)

    table.add_column("Product ID",      justify     =   "right", style = "bold blue on white")
    table.add_column("Product Name",    style       =   "bold red on blue")
    table.add_column("Expiration Date", justify     =   "center", style="bold white on red")

    for item in expired_products:
        table.add_row(item["product_id"], item["product_name"], item["expiration_date"])

    console = Console(record=True)
    console.print(table)

    if args.txt:
        print("The following text file has been created")
        console.save_text("expired.txt")


