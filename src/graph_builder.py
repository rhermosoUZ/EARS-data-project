import matplotlib.pyplot as plt
import networkx as nx

from data_builder import DataBuilder


class MusicGraph():
    
    def __init__(self, load_file=None) -> None:
        if load_file:
            print("Load graph from file")
            self.G = nx.read_graphml(load_file)
        else:
            self.db = DataBuilder()
            self.G = nx.Graph()
            self.add_integer_ids()
    
    def add_integer_ids(self):
        mbid_node_list = list(self.G.nodes)
        self.G = nx.convert_node_labels_to_integers(self.G)
        id_node_list = list(self.G.nodes)
        self.id_to_mbid = dict(zip(id_node_list, mbid_node_list))
        self.mbid_to_id = dict(zip(mbid_node_list, id_node_list))
    
    def build_graph(self, lastfmGraph=False):
        print("Construct graph ...")
        if lastfmGraph:
            self.db.store_lastfm()
            self.G.add_nodes_from(self.db.md.artists)
            self.G.add_nodes_from(self.db.md.users)
            self.G.add_edges_from(self.db.md.user_artist)
        else:
            self.db.store_all()
            self.G.add_nodes_from(self.db.md.artists)
            self.G.add_nodes_from(self.db.md.users)
            self.G.add_nodes_from(self.db.md.areas)
            self.G.add_nodes_from(self.db.md.labels)
            self.G.add_nodes_from(self.db.md.genres)
            self.G.add_edges_from(self.db.md.artist_area)
            self.G.add_edges_from(self.db.md.user_artist)
            self.G.add_edges_from(self.db.md.artist_labels)
            self.G.add_edges_from(self.db.md.artist_artist) # member_of
            self.G.add_edges_from(self.db.md.artist_genres)
            # self.G.add_nodes_from(self.db.md.albums)
            # self.G.add_edges_from(self.db.md.artist_album)
        
        self.db.print_stats()  
        print("Finished constructing graph ...")
        
    def print_stats(self):
        print("Number of nodes: {}".format(self.G.number_of_nodes()))
        print("Number of edges: {}".format(self.G.number_of_edges()))
        
    def save_graph(self, path):
        print("Saving graph as graphML file ...")
        nx.write_graphml(self.G, path)
        print("Finished saving graph as graphML file ...")
        self.draw_graph(self.G)
        
    def load_graph(self, path):
        print("Load graph from file")
        self.G = nx.read_graphml(path)
        
    def draw_graph(self, graph):
        nx.draw(self.G)
        plt.show()
    
    def reduce_by_min_degree(self, min_degree=1):
        remove_nodes = [node for node, degree in dict(self.G.degree()).items() if degree < min_degree]
        print("Removing {} Nodes ...".format(len(remove_nodes)))
        self.G.remove_nodes_from(remove_nodes)
    
    def get_subgraph(self, source):
        node_length = nx.single_source_shortest_path_length(self.G, source=source, cutoff=2)
        print(len(node_length))
        sub_nodes = list(node_length.keys())
        subG = self.G.subgraph(sub_nodes)
        return subG
        

if __name__ == "__main__":
    mg = MusicGraph()
    # mg.build_graph()
    # mg.reduce_by_min_degree(min_degree=2)
    # time_string = datetime.now().isoformat().replace(":","").replace(".", "")[:-5]
    # mg.save_graph("dataset/graph/musicgraph_{}.graphml".format(time_string))
    # mg.load_graph("dataset/graph/musicgraph_2022-04-11T2056432.graphml")
    # mg.print_stats()

    
    
        
