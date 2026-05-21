import sqlite3
import csv
import random
import path

class MusicBrainzProcessor:
    """Class  for processing MusicBrainz data dump and
    inserting data into a local sqlite database.
    """

    def __init__(self):
        self.con = sqlite3.connect(path.dbpath)
        self.cur = self.con.cursor()

    def artists(self):

        print("Creating artist table ...")

        self.cur.execute("DROP TABLE IF EXISTS artists")
        self.cur.execute("""
            CREATE TABLE artists (id INTEGER PRIMARY KEY, mbid TEXT, name TEXT, area INTEGER)
        """)

        print("Populating artist table using MusicBrainz data ...")

        with open(path.mbdump + '/artist') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab'):
                if line:
                    try:
                        area = int(line[11]) if line[11] != "\\N" else None
                        artist_id = int(line[0])
                        artist_mbid = line[1]
                        artist_name = line[2]
                        self.cur.execute("INSERT INTO artists VALUES (?, ?, ?, ?)", (artist_id, artist_mbid, artist_name, area))
                    except:
                        pass

        self.cur.execute("DELETE FROM artists WHERE name = (?)", ("Various Artists",))
        self.cur.execute("DELETE FROM artists WHERE name = (?)", ("[unknown]",))
        
        self.con.commit()

        print("Successfully created and populated artist table.")

    def artist_credits(self):

        print("Creating artist_credits table ...")

        self.cur.execute("DROP TABLE IF EXISTS artist_credits")
        self.cur.execute(
            "CREATE TABLE artist_credits (artist_credit_id INTEGER, artist_id Integer)")

        print("Populating artist_credits table using musicbrainz data ...")

        with open(path.mbdump + '/artist_credit_name') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONE):
                self.cur.execute("INSERT INTO artist_credits VALUES (:artist_credit_id, :artist_id)", {
                                 "artist_credit_id": line[0], "artist_id": line[2]})

        self.con.commit()

        print("Successfully created and populated artist_credit table.")

    def albums(self):

        print("Creating album table ...")

        self.cur.execute("DROP TABLE IF EXISTS albums")
        self.cur.execute(
            "CREATE TABLE albums (id INTEGER PRIMARY KEY, mbid TEXT, artist_credit_id INTEGER, name TEXT, year INTEGER)")

        print("Map releases to release year ...")
        release_to_year = {}
        with open(path.mbdump + '/release_group_meta') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab'):
                release_to_year[int(line[0])] = line[2]
        
        has_secondary = [False for i in range(5000000)]
        with open(path.mbdump + '/release_group_secondary_type_join') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab'):
                has_secondary[int(line[0])] = True
                
        has_official = [False for i in range(5000000)]
        with open(path.mbdump + '/release') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONE):
                if (line[5] != '\\N'):
                    if (int(line[5]) == 1):
                        has_official[int(line[4])] = True
                
        print("Populating album table using musicbrainz data ...")

        with open(path.mbdump + '/release_group') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONE):
                if len(line) < 2:
                    continue
                # Only add Albums(ID 1)
                if ((line[4] != '\\N')
                    and (int(line[4]) == 1)
                    and (has_official[int(line[0])])
                    and not (has_secondary[int(line[0])])):
                        self.cur.execute("INSERT INTO albums VALUES (:id, :mbid, :artist_credit_id, :name, :year)", {
                                         "id": line[0], "mbid": line[1], "artist_credit_id": int(line[3]), "name": line[2], "year": release_to_year[int(line[0])]})

        self.con.commit()

        print("Successfully created and populated album table.")

    def labels(self):
        print("Creating label table ...")

        self.cur.execute("DROP TABLE IF EXISTS labels")
        self.cur.execute(
            "CREATE TABLE labels (id INTEGER PRIMARY KEY, mbid TEXT, name TEXT, type_id INTEGER)")

        print("Populating label table using musicbrainz data ...")

        with open(path.mbdump + '/label') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONE):
                if len(line) < 1:
                    continue
                if line[10] != '\\N':
                    if int(line[10]) in [3,4,7]: # Publisher, Production, Original Production - see label_type table
                        self.cur.execute("INSERT INTO labels VALUES (?, ?, ?, ?)", (int(
                            line[0]), line[1], line[2], int(line[10])))
        
        self.cur.execute("DELETE FROM labels WHERE name = (?)", ("no label",))
        
        self.con.commit()

        print("Successfully created and populated label table.")
        print("")
    
    def areas(self):

        print("Creating area table ...")

        self.cur.execute("DROP TABLE IF EXISTS areas")
        self.cur.execute("CREATE TABLE areas (id INTEGER PRIMARY KEY, name TEXT)")

        print("Populating area table using musicbrainz data ...")

        with open(path.mbdump + '/area') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab'):
                if line:
                    if (line[11] == "\\N"):
                        line[11] = None
                    self.cur.execute(
                        "INSERT INTO areas VALUES (?, ?)", (int(line[0]), line[2]))

        self.con.commit()

        print("Successfully created and populated area table.")
        print("")

    def genres(self):
        
        print("Creating genres table ...")

        self.cur.execute("DROP TABLE IF EXISTS genres")
        self.cur.execute(
            "CREATE TABLE genres (id INTEGER, name TEXT)")

        print("Populating genres table using musicbrainz data ...")
        
        genre_set = set()
        with open(path.mbdump + '/genre') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONE):
                genre_set.add(line[2])
        
        with open(path.mbdump + '/tag') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONE):
                if (line[1] in genre_set):
                    self.cur.execute(
                        "INSERT INTO genres VALUES (?, ?)", (int(line[0]), line[1]))
        
        self.con.commit()
        
        print("Successfully created and populated genres table.")
       
    def r_artist_genre(self):
        print("Creating artist_genre table ...")

        self.cur.execute("DROP TABLE IF EXISTS artist_genres")
        self.cur.execute(
            "CREATE TABLE artist_genres (artist_id INTEGER, genre_id INT)")

        genre_set = set()
        with open(path.mbdump + '/genre') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONE):
                genre_set.add(line[2])
        
        genre_tag_map = {}
        with open(path.mbdump + '/tag') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONE):
                if (line[1] in genre_set):
                    genre_tag_map[line[0]] = line[1]
        
        with open(path.mbdump + '/artist_tag') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONE):
                if len(line) < 1:
                    continue
                artist_id = line[0]
                tag_id = line[1]
                if tag_id in genre_tag_map:
                    self.cur.execute(
                        "INSERT INTO artist_genres VALUES (?, ?)", (int(artist_id), int(tag_id)))
                    
        self.con.commit()
        
        print("Successfully created and populated artist genre table.") 
         
    def r_member_of(self):

        print("Creating member_of table ...")

        self.cur.execute("DROP TABLE IF EXISTS member_of")
        self.cur.execute(
            "CREATE TABLE member_of (artist_id TEXT, member_id TEXT)")

        print("Populating member_of table using musicbrainz data ...")

        member_links = [False for i in range(1000000)]
        with open(path.mbdump + '/link') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab'):
                if (len(line) < 1):
                    continue
                if (line[1] == "103"):
                    member_links[int(line[0])] = True
                    # member_links.append(line[0])

        with open(path.mbdump + '/l_artist_artist') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab'):
                if (len(line) < 1):
                    continue
                if (member_links[int(line[1])]):
                    self.cur.execute(
                        "INSERT INTO member_of VALUES (?, ?)", (int(line[2]), line[3]))

        self.con.commit()

        print("Successfully created and populated member_of table.")
        print("")

        
    def r_album_label(self):
        print("Creating album_label table ...")

        self.cur.execute("DROP TABLE IF EXISTS album_labels")
        self.cur.execute(
            "CREATE TABLE album_labels (album_id INTEGER, label_id INTEGER)")

        print("Mapping releases to albums ...")
        
        release_to_album = {}
        with open(path.mbdump + '/release') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONE):
                if len(line) < 1:
                    continue
                release_to_album[int(line[0])] = int(line[4])
                
                
        print("Populating album_label table using musicbrainz data ...")

        with open(path.mbdump + '/release_label') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONE):
                if len(line) < 1:
                    continue
                if (line[2] != '\\N'):
                    self.cur.execute("INSERT INTO album_labels VALUES (?, ?)", (
                        release_to_album[int(line[1])], int(line[2])))

        self.con.commit()

        print("Successfully created and populated album_label table.")
        print("")
   
    def close(self):
        self.con.close()

class LastFMProcessor:
    """Class used for processing Last.fm dump file and
    inserting data into a local sqlite database.
    """
    
    def __init__(self) -> None:
        self.con = sqlite3.connect(path.dbpath)
        self.cur = self.con.cursor()
        

    def clean_data(self):

        print("Loading MBIDs into memory...")

        # Alle gültigen MBIDs einmal laden
        self.cur.execute("SELECT mbid FROM artists")

        valid_mbids = {row[0] for row in self.cur.fetchall()}

        print(f"Loaded {len(valid_mbids)} MBIDs")

        input_file = path.lastfm + '/usersha1-artmbid-artname-plays.tsv'
        output_file = path.lastfm + '/sampled-usersha1-artmbid-artname-plays.tsv'

        n = 0

        with open(input_file, newline='', encoding='utf-8') as tsv_original:
            with open(output_file, 'w', newline='', encoding='utf-8') as tsv_clean:

                reader = csv.reader(
                    tsv_original,
                    dialect='excel-tab',
                    quoting=csv.QUOTE_NONE
                )

                for line in reader:

                    if len(line) < 4:
                        continue

                    mbid = line[1]

                    # Blitzschneller Hash-Lookup
                    if mbid in valid_mbids:

                        tsv_clean.write(
                            f"{line[0]}\t{line[1]}\t{line[2]}\t{line[3]}\n"
                        )

                        n += 1

                    #if n % 1000000 == 0:
                        #print(f"---- {n}")

    def users(self, min_plays=500):
        """Create the user table with each row consisting of 
        (user_sha, artist:mbid, plays) from the Last.fm dataset.

        Args:
            min_plays (int, optional): The minimum amount of plays a user has 
            for an artist to be imported into the database. Defaults to 500.
        """
        
        print("Creating users table ...")

        # (Re)create users table 
        self.cur.execute("DROP TABLE IF EXISTS users")
        self.cur.execute("CREATE TABLE users (user_sha TEXT, artist_mbid TEXT, plays INTEGER)")
        # self.cur.execute("CREATE INDEX artist_mbid ON users(artist_mbid)")
        
        print("Processing File ...")
        
        # For progress counter
        counter = 0
        #total_lines = 17559530 # line in lastfm file
        
        with open(path.lastfm + '/sampled-usersha1-artmbid-artname-plays.tsv') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONE):
                ############ PROGRESS COUNTER ##########
                counter += 1
                #if (counter % 1000000 == 0):
               #     print("{:10.2f}%".format((counter/total_lines)*100))
                ########################################
                plays = int(line[3])
                user_sha = line[0]
                artist_mbid = line[1]
                if(plays > min_plays):
                #    if counter %10000 == 0:
                    self.cur.execute("INSERT INTO users VALUES (?,?,?)", (user_sha, artist_mbid, plays))
        
        self.con.commit()

        print("Successfully created and populated users table.")
            
    def users_sample(self, sample_size=0.05, min_user_plays=20000, min_user_artists=40, artist_top_n=1, test_data_size=0.5):
        """Create a sample of the user data to obtain more manageable sized data in a meaningful way.
        The resulting table consists of (user_sha, artist:mbid, plays) rows.

        Args:
            sample_size (float, optional): The size of the sample from [0,1], with 1 = 100%.  Defaults to 0.05.
            min_user_plays (int, optional): The minimum of total recorded plays for a user to be considered. Defaults to 20000.
            min_user_artists (int, optional): The minimum of total artists a user has recorded plays for to be considered. Defaults to 40.
            artist_top_n (float, optional): The fraction of top played artists per user which are considered. Defaults to 1.
            test_data_size (float, optional): The size of the test data to be stored in users_sample_test. Has to be in [0,1]. Defaults to 0.5.
        """
        
        print("Creating users_sample table ...")

        self.cur.execute("DROP TABLE IF EXISTS users_sample")
        self.cur.execute("CREATE TABLE users_sample (user_sha TEXT, artist_mbid TEXT, plays INTEGER)")
        self.cur.execute("DROP TABLE IF EXISTS users_sample_train")
        self.cur.execute("CREATE TABLE users_sample_train (user_sha TEXT, artist_mbid TEXT, plays INTEGER)")
        self.cur.execute("DROP TABLE IF EXISTS users_sample_test")
        self.cur.execute("CREATE TABLE users_sample_test (user_sha TEXT, artist_mbid TEXT, plays INTEGER)")
        
        print("Reading Last.fm data file ...")
        
        # Read tsv-file and save data in memory.
        users = {}
        with open(path.lastfm + '/sampled-usersha1-artmbid-artname-plays.tsv') as tsv:
            for line in csv.reader(tsv, dialect='excel-tab', quoting=csv.QUOTE_NONE):
                user_sha = line[0]
                artist_mbid = line[1]
                plays = int(line[3])
                if user_sha not in users:
                    users[user_sha] = {"artists": {}, "plays": 0}
                users[user_sha]["artists"][artist_mbid] = plays
                users[user_sha]["plays"] += plays
                
        print("Process users and insert to table ...")
        
        for user in users:
            # sample user data by only using every record with x% chance
            if (random.random() <= sample_size):
                user_total_plays = users[user]["plays"]
                user_total_artists = len(users[user]['artists'])
                if (user_total_plays >= min_user_plays) and (user_total_artists >= min_user_artists):
                    sorted_artists = sorted(users[user]["artists"], key=users[user]["artists"].get, reverse=True)
                    # Consider top x% artists as favoured:
                    fav_artists = sorted_artists[:int(len(sorted_artists)*artist_top_n)]
                    # shuffle artists and split into train/test set.
                    random.shuffle(fav_artists)
                    artist_len = len(fav_artists)
                    fav_artists_train = fav_artists[:int(artist_len*(1-test_data_size))]
                    fav_artists_test = fav_artists[int(artist_len*(test_data_size)):]
                    for artist in fav_artists_train:
                        plays = users[user]["artists"][artist]
                        # Make sure that no field is empty
                        if (user and artist and plays):
                            self.cur.execute("INSERT INTO users_sample_train VALUES (?,?,?)", (user, artist, plays))
                            self.cur.execute("INSERT INTO users_sample VALUES (?,?,?)", (user, artist, plays))
                    for artist in fav_artists_test:
                        plays = users[user]["artists"][artist]
                        if (user and artist and plays):
                            self.cur.execute("INSERT INTO users_sample_test VALUES (?,?,?)", (user, artist, plays))
                            self.cur.execute("INSERT INTO users_sample VALUES (?,?,?)", (user, artist, plays))
        
        self.con.commit()

        print("Successfully created and populated users_sample table.")
    
    def close(self):
        self.con.close()
    
    
if __name__ == '__main__':
    
    # MusicBrainz
    mb = MusicBrainzProcessor()
    # mb.labels()
    # mb.genres()
    # mb.r_artist_genre()
    # ...
    mb.close()
    
    # Last.fm
    lfm = LastFMProcessor()
    lfm.clean_data()
    # lfm.users(min_plays=500)
    # lfm.users_sample(sample_size=0.05, min_user_plays=20000, artist_top_n=0.1)
    # lfm.users_sample(sample_size=0.05, min_user_plays=20000, min_user_artists=50, artist_top_n=0.4, test_data_size=0.5)
    lfm.close()
