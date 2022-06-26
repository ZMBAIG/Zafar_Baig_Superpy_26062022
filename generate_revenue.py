from rich.console import Console
console = Console()
from rich import print
import csv
from schedule_dates import to_get_datetime_object, to_get_change_day

def get_revenue_date(day):
    with open("sold.csv", "r") as sold_file:
        csv_reader          = csv.DictReader(sold_file)
        revenue             = 0
        for line in csv_reader:
            sell_date       = to_get_datetime_object(line["sell_date"])
            if sell_date    == day:
                revenue     += float(line["sell_price"])
        return round(revenue, 2)

def get_revenue_between_dates(day1, day2):
    with open("sold.csv", "r") as sold_file:
        csv_reader          = csv.DictReader(sold_file)
        revenue             = 0
        for line in csv_reader:
            sell_date       = to_get_datetime_object(line["sell_date"])
            if sell_date    >= day1 and sell_date <= day2:
                revenue     += float(line["sell_price"])
        return round(revenue, 2)

def to_generate_revenue(args, type_report="revenue"):
    if args.now:
        day                 = to_get_change_day(0)
        revenue             = get_revenue_date(day)
    if args.yesterday:
        day                 = to_get_change_day(-1)
        revenue             = get_revenue_date(day)
    if args.date:
        day                 = args.date[0].date()
        revenue             = get_revenue_date(day)
    if args.period:
        day1                = args.period[0].date()
        day2                = args.period[1].date()
        revenue             = get_revenue_between_dates(day1, day2)
    if type_report          == "revenue":
        if args.now:
            console.print(f"\n[bold white on green]The Total Revenue for today:[/]\n {day} = € {revenue}\n")
        if args.yesterday:
            console.print(f"\n[bold white on red]The Total Revenue for yesterday:[/]\n {day} = € {revenue}\n")
        if args.date:
            console.print(f"\n[bold white on blue]The Total Revenue on:[/]\n {day} = € {revenue}\n")
        if args.period:
            console.print(
                f"\n[bold blue on white]The Total Revenue from:[/]\n {day1} to {day2} = € {revenue}\n")
            
    return revenue
