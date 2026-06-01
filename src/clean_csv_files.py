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

if __name__ == "__main__":
    csv_directory = sys.argv[1] if len(sys.argv) > 1 else 'dataset/csv'
    remove_columns_from_csvs(csv_directory)
