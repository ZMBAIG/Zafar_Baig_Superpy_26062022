from rich.console import Console
console = Console()
from rich import print
from datetime import date, timedelta, datetime

# realtime-now
def to_get_current_date(args):
    today                   =   date.today()
    date_today              =   datetime.strftime(today, "%Y-%m-%d")
    with open("date_file.txt", "w") as date_file:
        date_file.write(date_today)
        console.print(f"[yellow]Welcome to real-time date:[/] {date_today}")
# advance-time
def to_get_advance_time(args):
    with open("date_file.txt", "r") as date_file:
        for line in date_file:
            old_date        = datetime.strptime(line, "%Y-%m-%d")
            delta           = timedelta(days=args.to_get_advance_time[0])
            new_date        = datetime.strftime((old_date + delta), "%Y-%m-%d")
            console.print(f"[blue]Welcome to advance-time date:[/], {new_date}")
        with open("date_file.txt", "w") as file:
            file.write(new_date)
# current date
def to_get_date_today():
    with open("date_file.txt", "r") as date_file:
        for line in date_file:
            return line
# Converting string to datetime object
def to_get_datetime_object(date_str):
    date_object = date.fromisoformat(date_str)
    return date_object

# Converting to different time
def to_get_change_day(number=None):
    now                     = to_get_date_today()
    delta                   = timedelta(days=number)
    return to_get_datetime_object(now) + delta
