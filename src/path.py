import os

current_dir = os.path.dirname(os.path.abspath(__file__))
home = os.path.abspath(os.path.join(current_dir, os.pardir))
dataset = os.path.join(home, 'dataset')
db = os.path.join(dataset, 'db')
graph = os.path.join(dataset, 'graph')
csv = os.path.join(dataset, 'csv')

# dont' change the following entries
dbpath = os.path.join(db, 'staging.db')
mbdump = os.path.join(home, 'resources', 'mbdump')
lastfm = os.path.join(home, 'resources', 'lastfm')
embeddings = os.path.join(home, 'embeddings')
evaluations = os.path.join(home, 'evaluations')

for output_dir in (db, graph, csv):
    os.makedirs(output_dir, exist_ok=True)
