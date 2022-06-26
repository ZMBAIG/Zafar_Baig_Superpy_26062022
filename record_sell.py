from rich.console import Console
console = Console()
from rich import print
import csv
from schedule_dates import to_get_date_today, to_get_datetime_object

# By creating a random unique item-ids in the following category; date(today), Number of items, Date of Expiration and Date of buy Items. Since products might have the same name, but could have a different unique-id, these products should be separated from each other in the inventory file.This makes a clear and meaning full property due to lack of copying same products.

def to_get_purchased_items():
    with open("bought.csv", "r") as bought_file:
        csv_reader = csv.DictReader(bought_file)
        purchased_items = [row for row in csv_reader]
        return purchased_items

def to_get_purchased_ids():
    with open("sold.csv", "r") as sold_file:
        csv_reader = csv.DictReader(sold_file)
        purchased_ids = [row["product_id"] for row in csv_reader]
        return purchased_ids

def to_get_existed_product(product_name):
    purchased_items         = to_get_purchased_items()
    purchased_ids           = to_get_purchased_ids()
    products_existence      = []
    today = to_get_date_today()
    today_date_object       = to_get_datetime_object(today)
    for item in purchased_items:
        expire_date_object        = to_get_datetime_object(item["expiration_date"])
        purchase_date_object   = to_get_datetime_object(item["purchase_date"])
        if (
            item["product_id"] not in purchased_ids
            and item["product_name"] == product_name
            and purchase_date_object <= today_date_object
            and expire_date_object >= today_date_object
        ):
            products_existence.append(item)
    if len(products_existence) == 0:
        console.print(f"\n[red]This product[/] {product_name}[red] does not exist in inventory or sold out.[/]")
    else:
        products_existence_sorted = sorted(
            products_existence, key=lambda x: x["expiration_date"]
        )
        return products_existence_sorted

def to_get_sell_item(args):
    today               = to_get_date_today()
    today_date_object   = to_get_datetime_object(today)
    products_existence  = to_get_existed_product(args.product_name[0].lower())
    products_to_sell    = []

    if products_existence:
        if args.amount > len(products_existence):
            console.print(
                f"[red]Not enough items of {args.product_name} to sell, only {len(products_existence)} item(s) left![/]"
            )
        else:
            for item in products_existence:
                expire_date_object = to_get_datetime_object(item["expiration_date"])
                if expire_date_object == today_date_object:
                    item["sell_price"]      = round(args.sell_price[0] * 0.65, 2)
                    item["sell_date"]       = today
                else:
                    item["sell_price"]      = args.sell_price[0]
                    item["sell_date"]       = today

                products_to_sell.append(item)

        with open("sold.csv", "a", newline="") as sold_file:
            fieldnames = [
                "product_id",
                "product_name",
                "sell_price",
                "amount",
                "sell_date",
                "expiration_date",
                "purchase_price",
                "purchase_date",
            ]

            csv_writer = csv.DictWriter(sold_file, fieldnames=fieldnames)
            csv_writer.writerows(products_to_sell[: args.amount])

            console.print(
                f'\n[bold red on white]Sold out: {args.amount} item(s) of {args.product_name[0]} for the price € {item["sell_price"]}\n'
            )
