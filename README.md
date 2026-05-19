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

## How to run

The project includes a `Makefile` with the most common dataset generation workflows. By default, `make` uses `.venv/bin/python`, but you can override it with the `PYTHON` variable if needed.

### Install dependencies

The project includes a `requirements.txt` file in the repository root with the Python dependencies from the virtual environment.

```bash
pip install -r requirements.txt
```

### Generate the sampled dataset

```bash
make generate_dataset
```

This runs `src/generate_dataset.py` with the default sampling and filtering values defined in the `Makefile`:

- `SAMPLE_SIZE=0.05`
- `MIN_USER_PLAYS=20000`
- `MIN_USER_ARTISTS=40`
- `ARTIST_TOP_N=1`
- `TEST_DATA_SIZE=0.5`

You can override any of these values directly from the command line:

```bash
make generate_dataset SAMPLE_SIZE=0.1 MIN_USER_PLAYS=10000 MIN_USER_ARTISTS=25
```

### Generate the dataset and GraphML graph

```bash
make generate_dataset_with_graph
```

This is equivalent to:

```bash
make generate_dataset GENERATE_GRAPH=True
```

It generates the sampled dataset and also builds the GraphML graph at `dataset/graph/musicgraph.graphml`.

### Generate the dataset, graph, and CSV exports

```bash
make generate_dataset_with_csv
```

This is equivalent to:

```bash
make generate_dataset GENERATE_GRAPH=True EXPORT_CSV=True
```

It generates the dataset, builds the GraphML graph, and exports grouped node and edge CSV files under `dataset/csv`.

### Export CSV files from an existing graph

```bash
make export_csv
```

This reads the GraphML file configured by `GRAPHML_FILE` and writes CSV files to `CSV_OUTPUT_DIR`. The defaults are:

- `GRAPHML_FILE=dataset/graph/musicgraph.graphml`
- `CSV_OUTPUT_DIR=dataset/csv`
- `NODE_TYPE_FIELD=type`
- `EDGE_TYPE_FIELD=relation`

Example using a custom graph path and output directory:

```bash
make export_csv GRAPHML_FILE=dataset/graph/custom.graphml CSV_OUTPUT_DIR=dataset/csv_custom
```

Boolean Make variables accept `True`, `true`, or `TRUE`.
