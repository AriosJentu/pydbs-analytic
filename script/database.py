"""
Module for special database operations.

This module facilitates interaction with databases, offering functionalities 
for creating databases using predefined schemas. Additionally, it includes 
methods for generating random data, primarily intended for testing purposes.


Classes:
    DBInterface: A class for interacting with databases.
"""

import sqlite3 
import random

from . import misc

class DBInterface:
    """
    DBInterface class for managing database connections and operations.

    Attributes:
        main_db_location    (str): The location of the main database.
        logging_db_location (str): The location of the logging database.
        connection          (sqlite3.Connection): The connection object 
                                                  to the main database.
        cursor              (sqlite3.Cursor): The cursor object for 
                                              executing SQL statements.

    Methods:
        - connect(): Establishes connection to the main and logging databases.
        - commit(): Commits the current transaction to the main database.
        - disconnect(): Disconnects from both the main and logging databases.
        - create_tables(): Creates tables in the main and logging databases.
        - fill_users(): Inserts dummy user data into the main database.
        - fill_blogs(): Inserts dummy blog data into the main database.
        - fill_logs_login_logout(): Inserts login or logout data into the 
                                    logging database.
        - fill_posts(): Inserts dummy post data into the main and logging 
                        databases.
        - fill_comments(): Inserts dummy comment data into the main and 
                           logging databases.
        - get_user_comments_info(): Retrieves user comments information 
                                    from the main database.
        - get_user_actions_info(): Retrieves user actions information 
                                   from the logging database.
    """

    def __init__(self, main_db_location: str, logging_db_location: str):
        """
        Initializes a DBInterface object with the specified database locations.

        Args:
            main_db_location    (str): The location of the main database.
            logging_db_location (str): The location of the logging database.
        """
        
        self.main_db_location = main_db_location
        self.logging_db_location = logging_db_location

        self.connection = None 
        self.cursor = None


    def connect(self) -> None:
        """
        Establishes connection to the main and logging databases.
        """

        self.connection = sqlite3.connect(self.main_db_location)
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            f"ATTACH DATABASE '{self.logging_db_location}' AS logging"
        )


    def commit(self) -> None:
        """
        Commits the current transaction to the main database.
        """

        self.connection.commit()


    def disconnect(self) -> None:
        """
        Disconnects from both the main and logging databases.
        """

        self.cursor.execute("DETACH logging")
        self.connection.close()

    
    def create_tables(self) -> None:
        """
        Creates tables in the main and logging databases in specialized schema.
        """

        query = """
            CREATE TABLE main.users (
                "id"            INTEGER NOT NULL PRIMARY KEY,
                "email"         TEXT,
                "login"         TEXT NOT NULL
            );
            CREATE TABLE main.blog (
                "id"            INTEGER NOT NULL PRIMARY KEY,
                "owner_id"      INTEGER,
                "name"          TEXT NOT NULL,
                "description"   TEXT,
                FOREIGN KEY("owner_id") REFERENCES "users"("id") 
                                        ON DELETE SET NULL
            );
            CREATE TABLE main.post (
                "id"            INTEGER NOT NULL PRIMARY KEY,
                "header"        TEXT NOT NULL,
                "text"          TEXT,
                "author_id"     INTEGER,
                "blog_id"       INTEGER,
                FOREIGN KEY("blog_id") REFERENCES "blog"("id") 
                                       ON DELETE SET NULL,
                FOREIGN KEY("author_id") REFERENCES "users"("id") 
                                         ON DELETE SET NULL
            );
            CREATE TABLE main.comment (
                "id"            INTEGER NOT NULL PRIMARY KEY,
                "text"          TEXT,
                "author_id"     INTEGER,
                "post_id"       INTEGER,
                FOREIGN KEY("post_id") REFERENCES "post"("id") 
                                       ON DELETE SET NULL,
                FOREIGN KEY("author_id") REFERENCES "users"("id") 
                                         ON DELETE SET NULL
            );
            CREATE TABLE logging.event_type (
                "id"            INTEGER NOT NULL PRIMARY KEY,
                "name"          TEXT NOT NULL
            );
            CREATE TABLE logging.space_type (
                "id"            INTEGER NOT NULL PRIMARY KEY,
                "name"          TEXT NOT NULL
            );
            CREATE TABLE logging.logs (
                "id"            INTEGER NOT NULL PRIMARY KEY,
                "datetime"      TEXT NOT NULL,
                "user_id"       INTEGER,
                "space_type_id" INTEGER,
                "event_type_id" INTEGER,
                FOREIGN KEY("event_type_id") REFERENCES "event_type"("id") 
                                             ON DELETE SET NULL,
                FOREIGN KEY("space_type_id") REFERENCES "space_type"("id") 
                                             ON DELETE SET NULL
            );
            INSERT INTO logging.event_type (name) 
            VALUES 
                ("login"), 
                ("comment"), 
                ("create_post"), 
                ("delete_post"), 
                ("logout");
            INSERT INTO logging.space_type (name) 
            VALUES ("global"), ("blog"), ("post");
        """

        self.connection.executescript(query)


    def __get_all_ids__(self, table_name: str = "main.users") -> list[int]:
        """
        Retrieves all IDs from the specified table.

        Args:
            table_name (str): The name of the table from which to retrieve IDs.

        Returns:
            list[int]: A list of all IDs from the specified table.
        """

        self.cursor.execute(f"SELECT id FROM {table_name}")
        return [pair[0] for pair in self.cursor.fetchall()]


    def fill_users(self, count: int = 1) -> None:
        """
        Inserts dummy user data into the main database.

        Args:
            count (int): The number of dummy users to insert.
        """

        logins = [misc.get_name() for _ in range(count)]
        emails = [
            name.lower().replace(" ", "_")+"@example.com" 
            for name in logins
        ]
        
        values = ", ".join([str(pair) for pair in zip(emails, logins)])
        query = f"INSERT INTO main.users (email, login) VALUES {values};"

        self.cursor.execute(query)
    

    def fill_blogs(self, count: int = 1) -> None:
        """
        Inserts dummy blog data into the main database.

        Args:
            count (int): The number of dummy blogs to insert.
        """

        user_ids = self.__get_all_ids__("main.users")
        
        values = ", ".join([
            f"({random.choice(user_ids)}, '{misc.get_sentence()}', \
                '{misc.get_description()}')" 
            for _ in range(count)
        ])

        query = f"""
            INSERT INTO main.blog (owner_id, name, description) VALUES {values};
        """

        self.cursor.execute(query)


    def fill_posts(self, count: int = 1) -> None:
        """
        Inserts dummy post data into the main and logging databases.

        Args:
            count (int): The number of dummy posts to insert.
        """

        user_ids = self.__get_all_ids__("main.users")
        blog_ids = self.__get_all_ids__("main.blog")

        values_main_lst = []
        values_logging_lst = []
        
        for _ in range(count):
            user_id = random.choice(user_ids)
            blog_id = random.choice(blog_ids)

            values_main_lst.append(
                f"('{misc.get_sentence()}', '{misc.get_description()}', \
                    {user_id}, {blog_id})"
            )
            values_logging_lst.append(
                f"('{misc.get_random_date('-2d', 'now')}', {user_id}, 2, 3)"
            )

            if random.randint(0, 3) == 1:
                #Randomly remove post
                values_logging_lst.append(
                    f"('{misc.get_random_date('+1d', '+4d')}', {user_id}, 2, 4)"
                )

        values_main = ", ".join(values_main_lst)
        values_logging = ", ".join(values_logging_lst)

        query_main = f"""
            INSERT INTO main.post (header, text, author_id, blog_id) 
            VALUES {values_main};
        """

        query_logging = f"""
            INSERT INTO logging.logs 
            (datetime, user_id, space_type_id, event_type_id) 
            VALUES {values_logging};
        """

        self.cursor.execute(query_main)
        self.cursor.execute(query_logging)

    
    def fill_comments(self, count: int = 1) -> None:
        """
        Inserts dummy comment data into the main and logging databases.

        Args:
            count (int): The number of dummy comments to insert.
        """

        user_ids = self.__get_all_ids__("main.users")
        post_ids = self.__get_all_ids__("main.post")

        values_main_lst = []
        values_logging_lst = []

        for _ in range(count):
            user_id = random.choice(user_ids)
            post_id = random.choice(post_ids)

            values_main_lst.append(
                f"('{misc.get_description()}', {user_id}, {post_id})"
            )
            values_logging_lst.append(
                f"('{misc.get_random_date('now', '+1d')}', \
                    {random.choice(user_ids)}, 3, 2)"
            )

        values_main = ", ".join(values_main_lst)
        values_logging = ", ".join(values_logging_lst)

        query_main = f"""
            INSERT INTO main.comment (text, author_id, post_id) 
            VALUES {values_main}
        """

        query_logging = f"""
            INSERT INTO logging.logs 
            (datetime, user_id, space_type_id, event_type_id) 
            VALUES {values_logging};
        """
        
        self.cursor.execute(query_main)
        self.cursor.execute(query_logging)


    def fill_logs_login_logout(self, is_login: bool = True) -> None:
        """
        Inserts login or logout data into the logging database.

        Args:
            is_login (bool): If True, inserts login data; otherwise, 
                             inserts logout data.
        """

        user_ids = self.__get_all_ids__("main.users")
        date_range = [("-5d", "now"), ("now", "+5d")][not is_login]
        state = 1 if is_login else 5

        values = ", ".join([
            f"('{misc.get_random_date(*date_range)}', {user_id}, 1, {state})"
            for user_id in user_ids
        ])

        query = f"""
            INSERT INTO logging.logs 
            (datetime, user_id, space_type_id, event_type_id) VALUES {values};
        """
       
        self.cursor.execute(query)

    
    def get_user_comments_info(self, username: str) -> list[tuple]:
        """
        Retrieves user comments information from the main database.

        Args:
            username (str): The username of the user whose comments 
                            information to retrieve.

        Returns:
            list[tuple]: A list of tuples containing user comments information.
        """

        query = f"""
            SELECT 
                usr.login AS Login,
                pst.header AS Header,
                (
                    SELECT usr_in.login 
                    FROM main.users AS usr_in 
                    WHERE usr_in.id == pst.author_id
                ) AS Author,
                (
                    SELECT count(*) 
                    FROM main.comment AS cmt_in 
                    WHERE cmt_in.post_id == cmt.post_id
                ) AS Count
            FROM
                main.comment AS cmt
                JOIN main.users AS usr ON cmt.author_id = usr.id
                JOIN main.post AS pst ON cmt.post_id = pst.id
            WHERE 
                usr.login == "{username}"
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()


    def get_user_actions_info(self, username: str) -> list[tuple]:
        """
        Retrieves user actions information from the logging database.

        Args:
            username (str): The username of the user whose actions 
                            information to retrieve.

        Returns:
            list[tuple]: A list of tuples containing user actions information.
        """

        query = f"""
            SELECT
                date(lgs.datetime) AS Date,
                count(CASE WHEN lgs.event_type_id == 1 THEN 1 END) AS Logins,
                count(CASE WHEN lgs.event_type_id == 5 THEN 1 END) AS Logouts,
                count(CASE WHEN lgs.space_type_id > 1 THEN 1 END) AS Actions
            FROM logging.logs AS lgs
            WHERE lgs.user_id == (
                SELECT usr.id FROM main.users AS usr 
                WHERE usr.login == "{username}" LIMIT 1
            )
            GROUP BY date(lgs.datetime)
        """

        self.cursor.execute(query)
        return self.cursor.fetchall()
