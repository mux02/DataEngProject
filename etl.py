import os
import glob
import psycopg2
import pandas as pd
from sql_queries import *


def process_song_file(cur, filepath):
    """ This function is used for reading JSON files in specific directory,
    and then inserting it these data into the database after proceecd it via
    several requirements (selected certain columns, convert to list, etc).
    
    Args:
        para1: the cursor object used for SQL queries and operations.
        para2: specific directory (song_data).
    Returns:
        Nothing.
    Raises:
        Nothing.
    """
    # open song file
    df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0].tolist()
    cur.execute(song_table_insert, song_data)
    
    # insert artist record
    artist_data = df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0].tolist()
    cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    """ This function performs a listing operation of all JSON files
    in a specific directory, which will be filled according to 'NextSong'
    action and the time values will be converted to certain units, then all of 
    these values will be inserted into the database (time table) after naming the 
    table columns, after that the 'user' data will be inserted into the user table.
    Finally, the function will be ready to insert 'songplay' table records.
    
    Args:
        para1: the cursor object used for SQL queries and operations.
        para2: specific directory (log_data).
    Returns:
        Nothing.
    Raises:
        Nothing.
    """
    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page.str.contains('NextSong')]

    # convert timestamp column to datetime
    t = pd.to_datetime(df['ts'], unit='ms')
    
    # insert time data records
    time_data = [t, t.dt.hour, t.dt.day, t.dt.week, t.dt.month, t.dt.year, t.dt.dayofweek]
    column_labels = ['ts','hour', 'day', 'week', 'month', 'year', 'dayofweek']
    time_df = pd.DataFrame(dict(zip(column_labels, time_data))) # 'dict' => convert into dictionary. and 'zip' => for specifying columns name and the data.

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = df[['userId','firstName','lastName','gender','level']]

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():
        
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        
        if results:
            songid, artistid = results
        else:
            songid, artistid = None, None

        # insert songplay record
        songplay_data = (pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """ This function will list all files in a specific directory
    and then process it with the right function whether it is a 
    log file or a song file. In addition, all files and operations 
    will be printed.
    
    Args:
        para1: the cursor object used for SQL queries and operations.
        para2: the connection object.
        para3: specific directory (log_data or song_data).
        para4: targeted function (process_song_file or process_log_file).
    Returns:
        Nothing.
    Raises:
        Print statement of each found and processed file.
    """
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    """ 
        This is the main function which will process_data function,
        and create the database connection plus the cursor object.
    """
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()