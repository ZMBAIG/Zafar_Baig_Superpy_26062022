from rich.console import Console
console = Console()
from rich import print
import csv
from schedule_dates import to_get_datetime_object, to_get_change_day
from generate_revenue import to_generate_revenue


def get_expenses_date(day):
    with open("bought.csv", "r") as bought_file:
        csv_reader          = csv.DictReader(bought_file)
        expenses            = 0
        for line in csv_reader:
            purchase_date   = to_get_datetime_object(line["purchase_date"])
            if purchase_date == day:
                expenses += float(line["purchase_price"])
        return round(expenses, 2)

def get_expenses_between_dates(day1, day2):
    with open("bought.csv", "r") as bought_file:
        csv_reader          = csv.DictReader(bought_file)
        expenses            = 0
        for line in csv_reader:
            purchase_date   = to_get_datetime_object(line["purchase_date"])
            if purchase_date >= day1 and purchase_date <= day2:
                expenses += float(line["purchase_price"])
        return round(expenses, 2)

def get_expenses(args):
    if args.now:
        day                 = to_get_change_day(0)
        expenses            = get_expenses_date(day)
    if args.yesterday:
        day                 = to_get_change_day(-1)
        expenses            = get_expenses_date(day)
    if args.date:
        day                 = args.date[0].date()
        expenses            = get_expenses_date(day)
    if args.period:
        day1                = args.period[0].date()
        day2                = args.period[1].date()
        expenses            = get_expenses_between_dates(day1, day2)
    return expenses

def get_profit(args):
    total_profit            = to_generate_revenue(args, type_report="profit") - get_expenses(args)
    profit                  = round(total_profit, 2)
    if args.now:
        day                 = to_get_change_day(0)
        console.print(f"\n[bold white on green]Total Profit/Loss on inventory stock for today,[/] {day}, = [bold red on white]€{profit}\n")
    if args.yesterday:
        day                 = to_get_change_day(-1)
        console.print(f"\n[bold white on green]Total Profit/Loss on inventory stock for yesterday,[/] {day}, = [blink bold red on white]€{profit}\n")
    if args.date:
        console.print(f"\n[bold white on green]Total Profit/Loss on inventory stock on[/] {args.date[0].date()} = [blink bold red on white]€{profit}\n")
    if args.period:
        console.print(
            f"\n[bold white on green]Total Profit/Loss on inventory stock for period between[/] {args.period[0].date()} and {args.period[1].date()} = [blink bold red on white]€{profit}\n"
        )
