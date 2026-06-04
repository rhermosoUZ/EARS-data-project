import sys
from pathlib import Path
import pandas as pd

def remove_columns_from_csvs(directory):

    columns_to_remove = ["id", "type", "relation"]

    directory = Path(directory)

    for csv_file in directory.glob("*.csv"):
        try:
            df = pd.read_csv(csv_file)

            # get existing columns
            existing_cols = [col for col in columns_to_remove if col in df.columns]

            if existing_cols:
                df = df.drop(columns=existing_cols)
                df.to_csv(csv_file, index=False)
                #print(f"{csv_file.name}: removed -> {existing_cols}")
            #else:
            #    print(f"{csv_file.name}: no columns found")

        except Exception as e:
            print(f"error at {csv_file.name}: {e}")


def rename_csv_headers_inplace(file_path, rename_map):
    df = pd.read_csv(file_path)
    df.rename(columns=rename_map, inplace=True)
    df.to_csv(file_path, index=False)


def reorder_csv_columns(file_path, column_order):
    df = pd.read_csv(file_path)
    df = df[column_order]
    df.to_csv(file_path, index=False)


if __name__ == "__main__":

    SCRIPT_DIR = Path(__file__).resolve().parent
    PROJECT_ROOT = SCRIPT_DIR.parent  # adjust if needed
    path = str(PROJECT_ROOT) + '/dataset/csv/'

    # remove redundant columns
    remove_columns_from_csvs(path)

    #rename columns
    rename_csv_headers_inplace(path + 'edges_member_of.csv', {"source" :"artist_mbid", "target": "artist_mbid"})
    rename_csv_headers_inplace(path + 'edges_hasLabel.csv', {"source": "artist_mbid", "target": "label_mbid"})
    rename_csv_headers_inplace(path + 'edges_hasGenre.csv', {"source": "artist_mbid", "target": "genre_name"})
    rename_csv_headers_inplace(path + 'edges_from_area.csv', {"source": "artist_mbid", "target": "area_name"})
    rename_csv_headers_inplace(path + 'edges_favours_artist.csv', {"target":"user_sha", "source": "artist_mbid"})
    reorder_csv_columns(path + 'edges_favours_artist.csv', ["user_sha", "artist_mbid",  "plays"])

    rename_csv_headers_inplace(path + 'nodes_label.csv', {"name": "label_name"})
    rename_csv_headers_inplace(path + 'nodes_genre.csv', {"name": "genre_name"})
    rename_csv_headers_inplace(path + 'nodes_artist.csv', {"name": "artist_name"})
    rename_csv_headers_inplace(path + 'nodes_area.csv', {"name": "area_name"})