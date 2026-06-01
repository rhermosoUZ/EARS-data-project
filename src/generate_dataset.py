import argparse
from datetime import datetime



### CONSTANTS ###
TIME_STRING = datetime.now().isoformat().replace(":","").replace(".", "")[:-5]
DEFAULT_USER_SAMPLE_PARAMETERS = {
    'sample_size': 0.05,
    'min_user_plays': 20000,
    'min_user_artists': 40,
    'artist_top_n': 1,
    'test_data_size': 0.5,
}

def data_processing(user_sample_parameters=None):
    """Process data in the MusicBrainz and Last.fm datasets and store them in SQLite database
    """
    import data_processing as dp

    if user_sample_parameters is None:
        user_sample_parameters = DEFAULT_USER_SAMPLE_PARAMETERS

    ### PROCESS MUSICBRAINZ DATA AND SAVE DATA IN LOCAL DATABASE ###

    mb = dp.MusicBrainzProcessor()
    mb.artists()
    mb.artist_credits()
    mb.albums()
    mb.labels()
    mb.areas()
    mb.genres()
    mb.r_artist_genre()
    mb.r_member_of()
    mb.r_album_label()
    mb.close()


    ### PROCESS LASTFM DATA AND SAVE DATA IN LOCAL DATABASE ###

    lfm = dp.LastFMProcessor()
    lfm.ensure_valid_MBIDs()
    #lfm.copy_user_profiles_to_db(min_plays=500)
    lfm.users_sample(**user_sample_parameters)


    ## SAMPLE LASTFM USERS INTO ANOTHER TABLE ###


    
def knowledge_graph():
    import path
    from graph_builder import MusicGraph

    ### BUILD FULL MUSIC GRAPH BASED ON SAMPLES USERS ###

    mg = MusicGraph()
    mg.build_graph()
    mg.save_graph(path.graph + "/musicgraph.graphml")

    ### BUILD LASTFM ONLY GRAPH BASED ON SAMPLED USERS ###

    #mg = MusicGraph()
    #mg.build_graph(lastfmGraph=True)
    #mg.save_graph(path.graph + "/lastfmgraph.graphml")

def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate the sampled dataset and optional graph files."
    )
    parser.add_argument(
        "--sample-size",
        type=float,
        default=DEFAULT_USER_SAMPLE_PARAMETERS["sample_size"],
        help="Fraction of eligible copy_user_profiles_to_db to sample. Default: %(default)s",
    )
    parser.add_argument(
        "--min-user-plays",
        type=int,
        default=DEFAULT_USER_SAMPLE_PARAMETERS["min_user_plays"],
        help="Minimum total recorded plays required for a user. Default: %(default)s",
    )
    parser.add_argument(
        "--min-user-artists",
        type=int,
        default=DEFAULT_USER_SAMPLE_PARAMETERS["min_user_artists"],
        help="Minimum number of distinct artists required for a user. Default: %(default)s",
    )
    parser.add_argument(
        "--artist-top-n",
        type=float,
        default=DEFAULT_USER_SAMPLE_PARAMETERS["artist_top_n"],
        help="Fraction of each sampled user's top artists to keep. Default: %(default)s",
    )
    parser.add_argument(
        "--test-data-size",
        type=float,
        default=DEFAULT_USER_SAMPLE_PARAMETERS["test_data_size"],
        help="Fraction of each sampled user's artists reserved for test data. Default: %(default)s",
    )
    parser.add_argument(
        "--build-graph",
        action="store_true",
        help="Build graph files after data processing.",
    )
    return parser.parse_args()

def user_sample_parameters_from_args(args):
    return {
        "sample_size": args.sample_size,
        "min_user_plays": args.min_user_plays,
        "min_user_artists": args.min_user_artists,
        "artist_top_n": args.artist_top_n,
        "test_data_size": args.test_data_size,
    }



if __name__ == '__main__':
    args = parse_args()
    data_processing(user_sample_parameters_from_args(args))
    if args.build_graph:
        knowledge_graph()

    
    



    
    
    
