import datetime


def today() -> str:
    """returns today's date in a human readable format

    Returns:
        str: todays date
    """
    date = datetime.datetime.now()
    # Define the format string
    date_format = "%A, %b %d %Y"
    # Use strftime to format the date

    date_str = date.strftime(date_format)

    return date_str
