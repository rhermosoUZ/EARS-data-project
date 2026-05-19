import argparse
import csv
import os
from collections import defaultdict

import path

DEFAULT_GRAPHML_FILE = os.path.join(path.graph, "musicgraph.graphml")
DEFAULT_OUTPUT_DIR = path.csv


def parse_args():
    parser = argparse.ArgumentParser(
        description="Export GraphML nodes and edges into grouped CSV files."
    )
    parser.add_argument(
        "--graphml-file",
        default=DEFAULT_GRAPHML_FILE,
        help="GraphML file to export. Default: %(default)s",
    )
    parser.add_argument(
        "--output-dir",
        default=DEFAULT_OUTPUT_DIR,
        help="Directory where CSV files are written. Default: %(default)s",
    )
    parser.add_argument(
        "--node-type-field",
        default="type",
        help="Node attribute used to group node CSV files. Default: %(default)s",
    )
    parser.add_argument(
        "--edge-type-field",
        default="relation",
        help="Edge attribute used to group edge CSV files. Default: %(default)s",
    )
    return parser.parse_args()


def export_graphml_to_csv(graphml_file, output_dir, node_type_field, edge_type_field):
    import networkx as nx

    os.makedirs(output_dir, exist_ok=True)

    graph = nx.read_graphml(graphml_file)

    nodes_by_type = defaultdict(list)
    for node_id, attrs in graph.nodes(data=True):
        node_type = attrs.get(node_type_field, "Unknown")
        row = {"id": node_id}
        row.update(attrs)
        nodes_by_type[node_type].append(row)

    for node_type, rows in nodes_by_type.items():
        csv_path = os.path.join(output_dir, f"nodes_{node_type}.csv")
        write_csv(csv_path, rows)
        print(f"Exported: {csv_path}")

    edges_by_type = defaultdict(list)
    for source, target, attrs in graph.edges(data=True):
        edge_type = attrs.get(edge_type_field, "Unknown")
        row = {
            "source": source,
            "target": target
        }
        row.update(attrs)
        edges_by_type[edge_type].append(row)

    for edge_type, rows in edges_by_type.items():
        csv_path = os.path.join(output_dir, f"edges_{edge_type}.csv")
        write_csv(csv_path, rows)
        print(f"Exported: {csv_path}")

    print("\nDone.")


def write_csv(csv_path, rows):
    if not rows:
        return

    fieldnames = []
    for row in rows:
        for key in row.keys():
            if key not in fieldnames:
                fieldnames.append(key)

    with open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    args = parse_args()
    export_graphml_to_csv(
        graphml_file=args.graphml_file,
        output_dir=args.output_dir,
        node_type_field=args.node_type_field,
        edge_type_field=args.edge_type_field,
    )
