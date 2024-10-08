#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# USAGE:
#   python lab1_part2.py music_small.db

import sys
import sqlite3
import timeit


# The database file should be given as the first argument on the command line
# Please do not hard code the database file!
db_file = sys.argv[1]


# The query to be optimized is given here
# It finds all the artists (ids and names) for which all of their albums received at least 50K listens
MY_QUERY = """SELECT artist.id, artist.artist_name, MIN(album.album_listens) as listens
	      FROM artist
	      INNER JOIN track ON track.artist_id = artist.id
	      INNER JOIN album ON track.album_id = album.id
	      GROUP BY artist.id
	      HAVING listens >= 50000"""

NUM_ITERATIONS = 100

def run_my_query(conn):
    for row in conn.execute(MY_QUERY):
        pass
    


# We connect to the database using
with sqlite3.connect(db_file) as conn:
    # We use a "cursor" to mark our place in the database.
    cursor = conn.cursor()

    # We could use multiple cursors to keep track of multiple
    # queries simultaneously.

    orig_time = timeit.repeat('run_my_query(conn)', globals=globals(), number=NUM_ITERATIONS)
    print("Before optimization:")

    print(f'Mean time: {sum(orig_time)/NUM_ITERATIONS:.3f} [seconds/query]')
    print(f'Best time: {min(orig_time)/NUM_ITERATIONS:.3f} [seconds/query]')

    # MAKE YOUR MODIFICATIONS TO THE DATABASE HERE
    
    # Create a composite index since there's no direct link between 
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_artist_id ON artist(id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_track_artist_id ON track(artist_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_track_album_id ON track(album_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_album_listens ON album(album_listens);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_album_id ON album(id);")

    create_index_sql = """CREATE INDEX idx_track_artist_album ON track(artist_id, album_id);"""
    create_album_id_index_sql = "CREATE INDEX IF NOT EXISTS idx_track_album_id ON track(album_id);"
    create_artist_id_index_sql = "CREATE INDEX IF NOT EXISTS idx_track_artist_id ON track(artist_id);"

    cursor.execute(create_album_id_index_sql)
    cursor.execute(create_artist_id_index_sql)
    cursor.execute(create_index_sql)


    new_time = timeit.repeat('run_my_query(conn)', globals=globals(), number=NUM_ITERATIONS)
    print("After optimization:")

    print(f'Mean time: {sum(new_time)/NUM_ITERATIONS:.3f} [seconds/query]')
    print(f'Best time   : {min(new_time)/NUM_ITERATIONS:.3f} [seconds/query]')
