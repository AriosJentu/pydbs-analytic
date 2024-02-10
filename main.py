import argparse
import sqlite3
from script import database, converter

def parse_args():
    decsr = "Get analytics from databases for users's login."
    parser = argparse.ArgumentParser(description=decsr)

    parser.add_argument("login", nargs="?", help="Specify the login")

    parser.add_argument("--authors-db", 
        default="authors.db",
        help="Location of Authors Database"
    )
    parser.add_argument("--logs-db", 
        default="logs.db",
        help="Location of Logging Database"
    )
    parser.add_argument("--comments-csv", 
        default="comments.csv",
        help="Output location for comments table"
    )
    parser.add_argument("--general-csv", 
        default="general.csv",
        help="Output location for general actions table"
    )

    parser.add_argument("-f", "--fill", 
        action="store_true", 
        help="Enable fill databases mode"
    )
    parser.add_argument("-g", "--create-tables",
        action="store_true",
        help="Create tables in databases"
    )
    parser.add_argument("-u", "--users-count",
        type=int,
        help="Add random users into database"
    )
    parser.add_argument("-b", "--blogs-count",
        type=int,
        help="Add random blogs into database"
    )
    parser.add_argument("-p", "--posts-count",
        type=int,
        help="Add random posts into database"
    )
    parser.add_argument("-c", "--comments-count",
        type=int,
        help="Add random comments into database"
    )
    parser.add_argument("-l", "--actions-count",
        type=int,
        help="Add random comments into database"
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    
    db_interface = database.DBInterface(args.authors_db, args.logs_db)
    db_interface.connect()

    if args.login:
        
        comments_list = db_interface.get_user_comments_info(args.login)
        actions_list = db_interface.get_user_actions_info(args.login)
        
        csv_writer = converter.CSVWriter(args.comments_csv, args.general_csv)
        csv_writer.write_comments(comments_list)
        csv_writer.write_general(actions_list)
    
    elif args.fill:

        if args.create_tables:
            try:
                db_interface.create_tables()
            except sqlite3.OperationalError:
                print("Tables already exist")
        
        if args.users_count:
            db_interface.fill_users(args.users_count)

        if args.blogs_count:
            db_interface.fill_blogs(args.blogs_count)

        if args.posts_count:
            db_interface.fill_posts(args.posts_count)

        if args.comments_count:
            db_interface.fill_comments(args.comments_count)

        if args.actions_count:
            for i in range(args.actions_count):
                db_interface.fill_logs_login_logout(True)
                db_interface.fill_logs_login_logout(False)

        db_interface.commit()

    db_interface.disconnect()
