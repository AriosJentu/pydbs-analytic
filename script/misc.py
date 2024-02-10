"""
Module providing utility functions for generating random data.

This module contains functions for generating random names, sentences, 
descriptions, and dates.

Attributes:
    is_lorem (bool): Indicates whether the lorem module is available.
    is_faker (bool): Indicates whether the faker module is available.

Functions:
    - get_name(): Generates a random name.
    - get_sentence(): Generates a random sentence.
    - get_description(): Generates a random description.
    - get_random_date(): Generates a random date within a specified range.
"""

import datetime

try:
    import lorem
    is_lorem = True
except ModuleNotFoundError:
    is_lorem = False

try:
    import faker
    is_faker = True 
except ModuleNotFoundError:
    is_faker = False

def get_name() -> str:
    """
    Generates a random name.

    Returns:
        str: A randomly generated name.
    """

    if not is_faker:
        return "User Name"
    
    return faker.Faker().name()


def get_sentence() -> str:
    """
    Generates a random sentence.

    Returns:
        str: A randomly generated sentence.
    """

    if not is_lorem:
        return "Random sentence"
    
    return lorem.sentence()


def get_description() -> str:
    """
    Generates a random description.

    Returns:
        str: A randomly generated description.
    """

    if not is_lorem:
        return "Random description"
    
    return lorem.paragraph()


def get_random_date(starts="-5d", ends="now") -> datetime.datetime:
    """
    Generates a random date within a specified range.

    Args:
        starts (str): The start date for the date range. 
                      Defaults to "-5d" (5 days ago).
        ends   (str): The end date for the date range. 
                      Defaults to "now" (current date and time).

    Returns:
        datetime.datetime: A randomly generated date and time.
    """

    if not is_faker:
        return datetime.datetime.now()
    
    return faker.Faker().date_time_between(start_date=starts, end_date=ends)
