
import math
import sqlite3
import path

#con = sqlite3.connect('dataset/db/staging.db')
con = sqlite3.connect(path.dbpath)

def mbid_to_artistname(mbid):
    cur = con.cursor()
    cur.execute("SELECT name FROM artists WHERE mbid = ?", [mbid])
    result = cur.fetchone()
    artistname = result[0]
    cur.close()
    return artistname

def mbid_to_labelname(mbid):
    cur = con.cursor()
    cur.execute("SELECT name FROM labels WHERE mbid = ?", [mbid])
    result = cur.fetchone()
    labelname = result[0]
    cur.close()
    return labelname

def get_rand_users(n):
    cur = con.cursor()
    cur.execute("SELECT user_sha FROM users_sample_train ORDER BY RANDOM() LIMIT ?", [n])
    result = cur.fetchall()
    cur.close()
    return result

def get_user_artist_mbids(user_sha):
    cur = con.cursor()
    cur.execute("SELECT artist_mbid, plays FROM users_sample_train WHERE user_sha = ?",
                [user_sha])
    user_artists = cur.fetchall()
    return user_artists

def get_test_user_artist_mbids(user_sha):
    cur = con.cursor()
    cur.execute("SELECT artist_mbid, plays FROM users_sample_test WHERE user_sha = ?",
                [user_sha])
    user_artists = cur.fetchall()
    return user_artists

def get_user_train_artists(user_sha):
    cur = con.cursor()
    cur.execute("SELECT artist_mbid, plays FROM users_sample_train WHERE user_sha = ?", [user_sha])
    user_artists = cur.fetchall()
    cur.close()
    return user_artists

def get_user_test_artists(user_sha):
    cur = con.cursor()
    cur.execute("SELECT artist_mbid FROM users_sample_test WHERE user_sha = ?", [user_sha])
    user_artists = cur.fetchall()
    cur.close()
    return user_artists

def get_test_artists():
    cur = con.cursor()
    cur.execute('''
                SELECT DISTINCT a.mbid
                    FROM users_sample_test us
                    INNER JOIN artists a ON us.artist_mbid = a.mbid;
                ''')
    user_artists = cur.fetchall()
    cur.close()
    return user_artists

def get_artist_popularity(total_items):
    cur = con.cursor()
    artists = dict()
    cur.execute("SELECT artist_mbid, user_sha FROM users_sample")
    results = cur.fetchall()
    for r in results:
        if  r[0] in artists:
            artists[r[0]] += 1
        else:
            artists[r[0]] = 1
    artist_popularities = {artist: -1 * math.log((artists[artist]/total_items), 2)
                        for artist in artists}
    cur.close()   
    return artist_popularities 

def confirmation(start_from):
    if start_from == 'full':
        print("You are about to resample the LastFM data. This will drop the current User Tables and replace them. Confirm the action by typing 'full reset'.")
        confirmation = input().lower()
        if confirmation != 'full reset':
            print("Process stopped. The pipeline will not but run.")
            return False
    return True
