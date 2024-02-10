"""
Module for write operations into CSV files.

This module provides functionality to write structured data to CSV files.
It includes methods for writing comments data and general data 
to separate CSV files.


Classes:
    CSVWriter: A class for interacting with CSV files.
"""

import csv

class CSVWriter:
    """
    A utility class for writing data to CSV files.

    Attributes:
        comments_dir (str): The directory path for writing comments data.
        general_dir  (str): The directory path for writing general data.

    Methods:
        - write_comments(): Writes comments data to a CSV file 
                            specified by comments_dir.
        - write_general(): Writes general actions data to a CSV file 
                           specified by general_dir.
    """

    def __init__(self, comments_dir: str, general_dir: str):
        """
        Initializes the CSVWriter instance.

        Args:
            comments_dir (str): The directory path for writing comments data.
            general_dir  (str): The directory path for writing general data.
        """

        self.comments_dir = comments_dir
        self.general_dir = general_dir


    def __writer__(self, 
            obj_dir: str, 
            field_names: list[str], 
            table: list[tuple]
    ):
        """
        Writes data to a CSV file.

        Args:
            obj_dir     (str): The directory path for the CSV file.
            field_names (list[str]): The list of field names for the CSV file.
            table       (list[tuple]): The data to be written to the CSV file.
        """

        with open(obj_dir, 'w', newline='') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=field_names)

            writer.writeheader()
            for row in table:
                writer.writerow(dict(zip(field_names, row)))


    def write_comments(self, table: list[tuple]):
        """
        Writes comments data to a CSV file.

        Args:
            table (list[tuple]): The comments data to be written.
        """

        field_names = ["login", "post_header", "post_author", "comments_count"]
        self.__writer__(self.comments_dir, field_names, table)


    def write_general(self, table: list[tuple]):
        """
        Writes general actions data to a CSV file.

        Args:
            table (list[tuple]): The general actions data to be written.
        """

        field_names = ["date", "logins", "logouts", "actions_count"]
        self.__writer__(self.general_dir, field_names, table)
