from pathlib import Path
import pandas as pd

def remove_columns_from_csvs(directory):
    """
    Lädt alle CSV-Dateien in einem Verzeichnis und entfernt die Spalten
    'id', 'type' und 'relation', falls vorhanden.

    Die Dateien werden überschrieben.
    """

    columns_to_remove = ["id", "type", "relation"]

    directory = Path(directory)

    for csv_file in directory.glob("*.csv"):
        try:
            df = pd.read_csv(csv_file)

            # Vorhandene Spalten ermitteln
            existing_cols = [col for col in columns_to_remove if col in df.columns]

            if existing_cols:
                df = df.drop(columns=existing_cols)
                df.to_csv(csv_file, index=False)
                print(f"{csv_file.name}: entfernt -> {existing_cols}")
            else:
                print(f"{csv_file.name}: keine passenden Spalten gefunden")

        except Exception as e:
            print(f"Fehler bei {csv_file.name}: {e}")