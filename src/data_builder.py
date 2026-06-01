import sqlite3
from queries import UserSampleQueries as q
import path

class DataBuilder():
    
    def __init__(self):
        self.con = sqlite3.connect(path.dbpath)
        self.cur = self.con.cursor()
        self.md = MusicData()
        
    def store_all(self):
        # self.store_albums_as_nodes()
        self.store_artists_as_nodes()
        self.store_users_as_nodes()
        # self.store_artist_album_relation()
        self.store_user_artist_relation()
        self.store_artist_area_relation()
        self.store_member_of_relation()
        self.store_artist_label_relation()
        self.store_artist_genre_relation()
    
    def store_albums_as_nodes(self):
        print("Store albums as nodes ...")
        self.cur.execute(q.albums)
        albums = self.cur.fetchall()
        album_nodes = [(album[1], {"type": "album", "mbid": album[1], "name": album[2], "year": str(album[3])}) for album in albums]
        self.md.albums.extend(album_nodes)
        
    def store_artists_as_nodes(self):
        print("Store artists as nodes ...")
        self.cur.execute(q.artists)
        artists = self.cur.fetchall()
        artist_nodes = [(artist[1], {"type": "artist", "mbid": artist[1], "name": artist[2]}) for artist in artists]
        self.md.artists.extend(artist_nodes)

    
    def store_users_as_nodes(self):
        print("Storesampled users as nodes ...")
        self.cur.execute(q.listenings_sampled)
        users = self.cur.fetchall()
        user_nodes = [(user[0], {"type": "user", "user_sha": user[0]}) for user in users]
        self.md.users.extend(user_nodes)
    
    def store_artist_album_relation(self):
        print("Store artist-album relation ...")
        self.cur.execute(q.r_artist_album)
        artist_albums = self.cur.fetchall()
        artist_album_relation = [(aa[0], aa[1], {"type": "relation", "relation": "has_album"}) for aa in artist_albums]
        self.md.artist_album.extend(artist_album_relation)

    def store_user_artist_relation(self):
        print("Store user-artist relation ...")
        self.cur.execute(q.listenings_sampled)
        users = self.cur.fetchall()
        user_artist_relation = [(user[0], user[1], {"type": "relation", "relation": "favours_artist", "plays": user[2]}) for user in users]
        self.md.user_artist.extend(user_artist_relation)
        
    def store_artist_area_relation(self):
        print("Store artist-area relation ...")
        self.cur.execute(q.artist_areas)
        artist_areas = self.cur.fetchall()
        areas = [(area[1], {"type": "area", "name": area[1]}) for area in artist_areas]
        artist_area_relation =[(aa[0], aa[1], {"type": "relation", "relation": "from_area"}) for aa in artist_areas]
        self.md.areas.extend(areas)
        self.md.artist_area.extend(artist_area_relation)
    
    def store_artist_genre_relation(self):
        print("Store artist-genre relation ...")
        self.cur.execute(q.artist_genres)
        artist_genres = self.cur.fetchall()
        unique_genres = {genre[1] for genre in artist_genres}
        genres = [(genre, {"type": "genre", "name": genre}) for genre in unique_genres] 
        genres = list(genres)
        artist_genre_relation =[(ag[0], ag[1], {"type": "relation", "relation": "hasGenre"}) for ag in artist_genres]
        self.md.genres.extend(genres)
        self.md.artist_genres.extend(artist_genre_relation)
        
    def store_artist_label_relation(self, min_label_degree=3):
        print("Store artist-label relation ...")
        self.cur.execute(q.labels)
        artist_labels_result = self.cur.fetchall()
        label_artists = {}
        label_names = {}
        for result in artist_labels_result:
            artist_id = result[0]
            label_id = result[1]
            label_name = result[2]
            if label_id not in label_artists:
                label_artists[label_id] = [artist_id]
                label_names[label_id] = label_name
            else:
                label_artists[label_id].append(artist_id)
        labels = []
        artist_labels_relation = []
        for label_id in label_artists:
            if len(label_artists[label_id]) > 3:
                labels.append(
                    (label_id, {"type": "label", "mbid": label_id, "name": label_names[label_id]})
                    )
                for artist in label_artists[label_id]:
                    artist_labels_relation.append(
                    (artist, label_id, {"type": "relation", "relation": "hasLabel"})    
                    )
        self.md.labels.extend(labels)
        self.md.artist_labels.extend(artist_labels_relation)
        
    def store_member_of_relation(self):
        print("Store member of relation ...")
        self.cur.execute(q.r_memberOf)
        member_of = self.cur.fetchall()
        member_of_relation =[(mo[0], mo[1], {"type": "relation", "relation": "member_of"}) for mo in member_of]
        self.md.artist_artist.extend(member_of_relation)
        
    def close_connection(self):
        self.con.close()
        


    
class MusicData():
    
    def __init__(self):
        # NODES
        self.albums = []
        self.artists = []
        self.users = []
        self.areas = []
        self.labels = []
        self.genres = []
    
        # EDGES
        self.artist_album = []   
        self.user_artist = []
        self.artist_area = []
        self.artist_artist = []
        self.artist_labels = []
        self.artist_genres = []
        
        
if __name__ == '__main__':
    db = DataBuilder()
    # db.store_all()
    # db.store_artist_label_relation()
    # db.print_stats()
    db.close_connection()