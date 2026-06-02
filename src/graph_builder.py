import networkx as nx

from data_builder import DataBuilder

class MusicGraph:

    def __init__(self) -> None:
        self.db = DataBuilder()
        self.G = nx.Graph()
        self.add_integer_ids()

    def add_integer_ids(self):
        mbid_node_list = list(self.G.nodes)
        self.G = nx.convert_node_labels_to_integers(self.G)
        id_node_list = list(self.G.nodes)
        self.id_to_mbid = dict(zip(id_node_list, mbid_node_list))
        self.mbid_to_id = dict(zip(mbid_node_list, id_node_list))

    def build_graph(self):
        print("Construct graph ...")
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

        self.print_stats()
        print("Finished constructing graph ...")

    def print_stats(self):
        print("Number of nodes: {}".format(self.G.number_of_nodes()))
        print("Number of edges: {}".format(self.G.number_of_edges()))

    def save_graph(self, path, draw=False, draw_path=None):
        print("Saving graph as graphML file ..." + path)
        nx.write_graphml(self.G, path)
        print("Finished saving graph as graphML file ...")
        if draw:
            self.draw_graph(self.G, output_file=draw_path, show=draw_path is None)

    def load_graph(self, path):
        print("Load graph from file")
        self.G = nx.read_graphml(path)

    def draw_graph(self, graph=None, max_nodes=500, output_file=None, show=True):
        graph = graph or self.G
        node_count = graph.number_of_nodes()
        edge_count = graph.number_of_edges()
        if node_count > max_nodes:
            print(
                "Graph has {} nodes and {} edges. Skipping drawing because "
                "NetworkX layout rendering is too slow for large graphs. "
                "Use get_subgraph(...) or increase max_nodes to draw a smaller view."
                .format(node_count, edge_count)
            )
            return

        import matplotlib.pyplot as plt

        nx.draw(graph, with_labels=False, node_size=20, width=0.2)
        if output_file:
            plt.savefig(output_file, dpi=150, bbox_inches="tight")
        if show:
            plt.show()
        plt.close()

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

    def count_nodes_of_type(self, node_type):
         return sum(
            1
            for _, data in self.G.nodes(data=True)
            if data.get("type") == node_type
        )

    def count_edges_between_types(self, type_a, type_b):
        count = 0
        for u, v in self.G.edges():
            u_type = self.G.nodes[u].get("type")
            v_type = self.G.nodes[v].get("type")

            # count both directions
            if (
                    (u_type == type_a and v_type == type_b)
                    or
                    (u_type == type_b and v_type == type_a)
            ):
                count += 1
        return count


    def print_stats(self):
        node_stats = {
            'albums':self.count_nodes_of_type('album'),
            'artists': self.count_nodes_of_type('artist'),
            'copy_user_profiles_to_db': self.count_nodes_of_type('user'),
            'areas': self.count_nodes_of_type('area'),
            'labels': self.count_nodes_of_type('label'),
            'genres': self.count_nodes_of_type('genre')
        }
        edge_stats = {
            'artist_album': self.count_edges_between_types('artist', 'album'),
            'user_artist': self.count_edges_between_types('user', 'artist'),
            'artist_area': self.count_edges_between_types('artist', 'area'),
            'artist_artist': self.count_edges_between_types('artist', 'artist'),
            'artist_labels': self.count_edges_between_types('artist', 'label'),
            'artist_genres': self.count_edges_between_types('artist', 'genre')
        }
        print("---------------------")
        print("Graph Stats:")
        print("---------------------")
        print("Total Nodes:\t\t {}".format(sum(node_stats.values())))
        print("Total Edges:\t\t {}".format(sum(edge_stats.values())))
        print("---------------------")
        print("# Albums:\t\t {}".format(node_stats['albums']))
        print("# Artists:\t\t {}".format(node_stats['artists']))
        print("# Users:\t\t {}".format(node_stats['copy_user_profiles_to_db']))
        print("# Areas:\t\t {}".format(node_stats['areas']))
        print("# Labels:\t\t {}".format(node_stats['labels']))
        print("# Genres:\t\t {}".format(node_stats['genres']))
        print("---------------------")
        # print("# Artist-Album Relations:\t\t {}".format(edge_stats['artist_album']))
        print("# User-Artist Relations:\t\t {}".format(edge_stats['user_artist']))
        print("# Artist-Area Relations:\t\t {}".format(edge_stats['artist_area']))
        print("# Artist-Artist Relations:\t\t {}".format(edge_stats['artist_artist']))
        print("# Artist-Label Relations:\t\t {}".format(edge_stats['artist_labels']))
        print("# Artist-Genre Relations:\t\t {}".format(edge_stats['artist_genres']))


if __name__ == "__main__":
    mg = MusicGraph()
    mg.build_graph()
    # mg.reduce_by_min_degree(min_degree=2)
    # time_string = datetime.now().isoformat().replace(":","").replace(".", "")[:-5]
    # mg.save_graph("dataset/graph/musicgraph_{}.graphml".format(time_string))
    # mg.load_graph("dataset/graph/musicgraph_2022-04-11T2056432.graphml")
    # mg.print_stats()
