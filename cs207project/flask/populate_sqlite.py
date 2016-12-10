# populate_sqlite.py
# (c) Jonne Saleva, Nathaniel Burbank, Nicholas Ruta, Rohan Thavarajah

import pandas.io.sql as pd_sql
import pandas as pd
import sqlite3

def main():
    """
    Populates SQLite database.
    """
    with sqlite3.connect('ts_metadata.sqlite') as conn:
        pd.read_csv('ts_metadata.txt', sep=' ')\
          .to_sql('ts_metadata', conn, index=False)

if __name__ == '__main__':
    main()
