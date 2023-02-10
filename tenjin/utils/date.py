import datetime

def today() -> str:
    date = datetime.datetime.now()
    # Define the format string
    date_format = "%A, %b %d%t %Y"
    # Use strftime to format the date

    date_str = date.strftime(date_format)

    # Add the suffix "th" to the day of the month
    if 4 <= date.day % 100 <= 20:
        date_str = date_str.replace("%t", "th")
    else:
        date_str = date_str.replace("%t", ["st", "nd", "rd"][date.day % 10 - 1])

    return date_str