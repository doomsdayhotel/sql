#!/usr/bin/env python
# -*- encoding: utf-8 -*-

# USAGE:
#   python lab1_part1.py music_small.db

import sys
import sqlite3


# The database file should be given as the first argument on the command line
# Please do not hard code the database file!
db_file = sys.argv[1]

# We connect to the database using 
with sqlite3.connect(db_file) as conn:
    # This query counts the number of artists who became active in 1990
    year = (1990,)
    for row in conn.execute('SELECT count(*) FROM artist WHERE artist_active_year_begin=?', year):
        # Since there is no grouping here, the aggregation is over all rows
        # and there will only be one output row from the query, which we can
        # print as follows:
        print('Tracks from {}: {}'.format(year[0], row[0]))
        
        # The [0] bits here tell us to pull the first column out of the 'year' tuple
        # and query results, respectively.

    # ADD YOUR CODE STARTING HERE
    
    # Question 1
    print('\nQuestion 1:')
    print('---')
    
    # implement your solution to q1

    query = "SELECT id, track_title FROM track WHERE track_lyricist LIKE ?"
    pattern = 'W%'

    for row in conn.execute(query, [pattern]):
        print('Track id: {}, track title: {}'.format(row[0], row[1]))
    
    # Question 2
    print('\nQuestion 2:')
    print('---')
    
    # implement your solution to q2
    for row in conn.execute('SELECT DISTINCT track_explicit FROM track where track_explicit is not NULL'):
        print('Possible values: {}'.format(row[0]))
    
    # Question 3
    print('\nQuestion 3:')
    print('---')
    
    # implement your solution to q3
    for row in conn.execute('SELECT id, track_title FROM track WHERE track_listens = (SELECT MAX(track_listens) FROM track)'):
        print('Track id: {}, Track title: {}'.format(row[0], row[1]))
    
    # Question 4
    print('\nQuestion 4:')
    print('---')
    
    # implement your solution to q4
    for row in conn.execute('SELECT count(id) FROM artist WHERE artist_related_projects IS NOT NULL'):
        print('Number of artists with related projects: {}'.format(row[0]))
    
    # Question 5
    print('\nQuestion 5:')
    print('---')
    
    # implement your solution to q5
    num_tracks = 4
    query = "SELECT track_language_code, COUNT(*) as count FROM track GROUP BY track_language_code HAVING COUNT(*) = ?"

    for row in conn.execute(query, (num_tracks,)):
        print('Language code: {}'.format(row[0]))
    
    # Question 6
    print('\nQuestion 6:')
    print('---')
    
    # implement your solution to q6
    pattern = '199_'
    query = "SELECT count(t.id) FROM artist a LEFT JOIN track t ON a.id = t.artist_id WHERE a.artist_active_year_begin LIKE ? and a.artist_active_year_end  LIKE ?"

    for row in conn.execute(query, [pattern, pattern]):
        print('{} tracks are by artists known to be active only within the 1990s.'.format(row[0]))
    
    # Question 7
    print('\nQuestion 7:')
    print('---')
    
    # implement your solution to q7
    for row in conn.execute('SELECT ar.id, ar.artist_name , COUNT (DISTINCT al.album_producer) as unique_producers FROM track t LEFT JOIN album al ON t.album_id = al.id LEFT JOIN artist ar ON t.artist_id = ar.id WHERE album_producer IS NOT NULL GROUP BY 1,2 ORDER BY unique_producers DESC LIMIT 3'):
        print(f"ID: {row[0]}, Name: {row[1]}")
    
    # Question 8
    print('\nQuestion 8:')
    print('---')
    
    # implement your solution to q8
    for row in conn.execute('SELECT t.id, t.track_title, ar.artist_name, (al.album_listens - t.track_listens) AS diff FROM track t JOIN album al ON t.album_id = al.id JOIN artist ar ON t.artist_id = ar.id ORDER BY diff DESC LIMIT 1;'):
        print('Track ID: {}, Track title: {}, Artist name: {}'.format(row[0], row[1], row[2]))
