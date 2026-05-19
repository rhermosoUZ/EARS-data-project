# Music dataset from open data sources
The dataset contains a collaborative music knowledge graph built from MusicBrainz and Last.fm, including users, artists, genres, labels, and areas, with listening and semantic relationships provided in CSV and GraphML formats.

## /dataset/db

Contains the whole SQLite database as a single file. Can be loaded using sqlite3 and is accessed by the recommender system.


## /dataset/graph

Is where the system stores knowledge graphs in graphml-format. Contains the pre-computed graphs as used in the master thesis

## /resources

Includes the datasets and the SQL-file for creating the full MusicBrainz Database Schema

### /resources/lastfm

The Last.fm dataset downloaded from :
https://ocelma.net/MusicRecommendationDataset/lastfm-360K.html

### /resources/mbdump

The mbdump and mbdump-derived data dumps from MusicBrainz. 
Only the tables used by the recommender system are contained. The full data (~16GB) can be downloaded here:
https://musicbrainz.org/doc/MusicBrainz_Database/Download

## /results

Contains produced results which were used for the master thesis. The folder is not need for the recommender system to work.

## /src

Source code of the artist recommender. Generally follows the components as discussed in the master thesis. The generate_dataset.py script generates the sampled dataset used by the recommender, and export_into_csv_files.py exports GraphML nodes and edges into grouped CSV files under `dataset/csv`.

## Make targets

Run `make generate_dataset` to generate the dataset, `make generate_dataset_with_graph` to also build `dataset/graph/musicgraph.graphml`, `make generate_dataset_with_csv` to build the graph and export CSV files, or `make export_csv` to export CSV files from an existing GraphML file. Boolean Make variables use `True` or `False`, for example `make generate_dataset GENERATE_GRAPH=True EXPORT_CSV=True`.
