"""
This module contains all the method or class which make
common patterns shorter and easier
"""

from datetime import datetime


def date_filter(date):
    """
    Format the datetime object to string form
    :param date: datetime object
    :return: string
    """
    if not isinstance(date, datetime):
        raise ValueError("Invalid data type")

    return date.strftime("%B %d, %Y")
