
class UserSampleQueries():
    """Query data which is somehow associated with the sampled user data from Last.fm
    """
    
    albums = '''
        SELECT DISTINCT al.id, al.mbid, al.name, al.year
            FROM users_sample us
            INNER JOIN artists a ON us.artist_mbid = a.mbid
            INNER JOIN artist_credits ac ON a.id = ac.artist_id
            INNER JOIN albums al ON ac.artist_credit_id = al.artist_credit_id;
        '''

    artists = '''
        SELECT DISTINCT a.id, a.mbid, a.name, a.area
            FROM users_sample us
            INNER JOIN artists a ON us.artist_mbid = a.mbid;
        '''
        
    training_artists = '''
        SELECT DISTINCT a.id, a.mbid, a.name, a.area
            FROM users_sample_train us
            INNER JOIN artists a ON us.artist_mbid = a.mbid;
        '''      
        
    test_artists = '''
        SELECT DISTINCT a.id, a.mbid, a.name, a.area
            FROM users_sample_test us
            INNER JOIN artists a ON us.artist_mbid = a.mbid;
        '''   
          
    artist_areas = ''' 
        SELECT DISTINCT a.mbid AS artist_mbid, areas.name AS area
            FROM users_sample us
            INNER JOIN artists a ON us.artist_mbid = a.mbid
            INNER JOIN areas ON a.area = areas.id;
    '''
        
    r_artist_album = '''
        SELECT DISTINCT a.mbid AS artist, al.mbid AS album
            FROM users_sample us
            INNER JOIN artists a ON us.artist_mbid = a.mbid
            INNER JOIN artist_credits ac ON a.id = ac.artist_id
            INNER JOIN albums al ON ac.artist_credit_id = al.artist_credit_id;
        '''
        
    r_memberOf = '''
            SELECT DISTINCT a.mbid AS artist, b.mbid AS band
                FROM member_of mo 
                INNER JOIN artists a ON a.id = mo.artist_id 
                INNER JOIN artists b ON b.id = mo.member_id
                INNER JOIN users_sample us1 ON us1.artist_mbid = a.mbid
                INNER JOIN users_sample us2 ON us2.artist_mbid = b.mbid
        '''
        
    labels = '''
        SELECT DISTINCT a.mbid AS artist_mbid, l.mbid AS label_mbid, l.name AS label_name
            FROM users_sample us
            INNER JOIN artists a ON us.artist_mbid = a.mbid
            INNER JOIN artist_credits ac ON a.id = ac.artist_id
            INNER JOIN albums al ON ac.artist_credit_id = al.artist_credit_id
            INNER JOIN album_labels alab ON al.id = alab.album_id 
            INNER JOIN labels l ON alab.label_id = l.id;
        '''
        
    artist_genres = '''
        SELECT DISTINCT a.mbid AS artist, g.name AS genre
            FROM users_sample us
            INNER JOIN artists a ON us.artist_mbid = a.mbid
            INNER JOIN artist_genres ag ON a.id = ag.artist_id
            INNER JOIN genres g ON ag.genre_id = g.id;
    '''
        
    users_sample = '''
        SELECT user_sha, artist_mbid, plays 
            FROM users_sample_train;
        '''