# User Analytics Provider

This script provides functionality to retrieve analytics from databases for users login, as well as to fill databases with random data.

## Usage

```bash
python main.py [login] [-f] [-g] [-u USERS_COUNT] [-b BLOGS_COUNT] [-p POSTS_COUNT] [-c COMMENTS_COUNT] [-l ACTIONS_COUNT] [--authors-db AUTHORS_DB] [--logs-db LOGS_DB] [--comments-csv COMMENTS_CSV] [--general-csv GENERAL_CSV]
```

## Arguments

- `login`: Specify the user login for which analytics should be retrieved.
- `-f`, `--fill`: Enable fill databases mode.
- `-g`, `--create-tables`: Create tables in databases.
- `-u USERS_COUNT`: Add random users into the database.
- `-b BLOGS_COUNT`: Add random blogs into the database.
- `-p POSTS_COUNT`: Add random posts into the database.
- `-c COMMENTS_COUNT`: Add random comments into the database.
- `-l ACTIONS_COUNT`: Add random actions into the database.
- `--authors-db AUTHORS_DB`: Location of Authors Database. Default: `authors.db`.
- `--logs-db LOGS_DB`: Location of Logging Database. Default: `logs.db`.
- `--comments-csv COMMENTS_CSV`: Output location for comments table. Default: `comments.csv`.
- `--general-csv GENERAL_CSV`: Output location for general actions table. Default: `general.csv`.

## Examples

1. Get analytics for a specific user:
```bash
python main.py <login>
```
2. Enable fill databases mode and create tables:
```bash
python main.py --fill -g
```
3. Add random users, blogs, posts, comments, and actions:
```bash
python main.py --fill -u 10 -b 5 -p 20 -c 50 -l 3
```
4. Specify custom database and CSV file locations:
```bash
python main.py <login> --authors-db custom_authors.db --logs-db custom_logs.db --comments-csv custom_comments.csv --general-csv custom_general.csv
```