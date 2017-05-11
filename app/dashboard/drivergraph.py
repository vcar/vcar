from __future__ import print_function
from __future__ import unicode_literals
import os
import copy
import json
import yaml
from random import choice
import networkx as nx
from networkx.drawing.nx_pydot import write_dot, read_dot
from networkx.readwrite import json_graph
import networkx.algorithms.isomorphism as iso

from .constants import DefaultSettings
from .constants import DATA, WEIGHT, COLORS

# ___________________________ Start : DriverGraph ___________________________ #


class DriverGraph:
    """ this class create a driver graph using registred
        driver traces, after an abstraction algorithm wich
        is configured using the settings configuration
    """

    def __init__(self, **kwargs):
        """inisialize the DriverGraph"""
        self.name = kwargs.get('name', 'Driver Bihavior Graph')
        self.settings = kwargs.get('settings', DefaultSettings)
        self.max_nodes = kwargs.get('max_nodes', None)
        self.node_id = kwargs.get('init_node', 0)
        self.G = kwargs.get('graph', None)
        self.last_id = 0
    # ====================================================================== #

    @property
    def settings(self):
        return self.settings

    @settings.setter
    def settings(self, settings):
        self.settings = settings
    # ====================================================================== #

    def __str__(self):
        return "<DriverGraph name: {}, time: {}, settings: {}>".format(
            self.name, self.time, self.settings
        )
    # ====================================================================== #

    def show_attributes(self):
        """Show DriverGraph attributes"""
        print("\nATTRIBUTES:")
        for node_id, attributes in self.G.nodes(data=True):
            print("Node {} :: [".format(node_id), end='')
            for name, value in attributes.items():
                print("{} |".format(value), end=' ')
            print("]")

    def show_edges(self):
        """Show DriverGraph edges"""
        print("\nEDGES :")
        for id1, id2 in self.G.edges():
            print("({}, {}, {})".format(
                id1, id2, self.G[id1][id2]['weight']
            ), end=', ')

    def debug(self, id=None):
        if id is None:
            for node_id, attributes in self.G.nodes(data=True):
                print('-------------- Node {} --------------'.format(node_id))
                for att, value in attributes.items():
                    print(">>[[{}]] {} : {}".format(id, att, value))
        else:
            print('.', end="")

    def graph_summary(self):
        print("\nNodes: {}".format(len(self.G.nodes(data=True))))
        print("\nEdges: {}".format(len(self.G.edges())))
    # ====================================================================== #

    def create_digraph(self, filename=None):
        """Create a Directed Graph from the openxc traces"""
        if filename is None:
            raise ValueError('Plz provide an openxc trace file.')

        data = DATA
        self._init_graph()
        with open(filename, 'r') as f:
            for line in f:
                temp = json.loads(line)
                signal = temp.get('name')
                value = self._invoke_ranges(signal, temp.get('value'))
                if value is None:
                    continue
                data = copy.deepcopy(data)
                if signal in data:
                    data[signal] = str(value)
                if self._create_node(data) is False:
                    break
        print('Done')
    # ====================================================================== #

    def build_digraph(self, res=None):
        """Create a Directed Graph from Elasticsearch"""

        data = DATA
        self._init_graph()
        for hit in res['hits']['hits']:
            signal = hit["_source"]['name']
            value = self._invoke_ranges(signal, hit["_source"]['value'])
            if value is None:
                continue
            data = copy.deepcopy(data)
            if signal in data:
                data[signal] = str(value)
            if self._create_node(data) is False:
                break

    # ====================================================================== #

    def _create_node(self, data):
        """Create node if doesn't exist, and create or update edges"""
        if self.max_nodes is not None and self.node_id >= self.max_nodes:
            return False
        id = self._find_node(data)
        # self.debug(self.node_id)
        if id is None:
            self.node_id += 1
            self.G.add_node(self.node_id, data)
            self.G.add_edge(self.last_id, self.node_id, weight=WEIGHT)
            # print(self.G.nodes())
            # print(self.G.edges())
            self.last_id = self.node_id
            # print(self.node_id, self.last_id)
        else:
            if self.G.has_edge(self.last_id, id):
                # print("Edge exist")
                self.G[self.last_id][id]['weight'] += WEIGHT
            else:
                pass
                # print("New Edge")
                self.G.add_edge(self.last_id, id, weight=WEIGHT)
            # print(self.G.edges())
            self.last_id = id
    # ====================================================================== #

    def _init_graph(self):
        """ inisialize the graph with the first ZERO node"""
        # self.G = nx.DiGraph(name=self.name)
        self.G = nx.DiGraph()
        self.G.add_node(self.node_id, DATA)
    # ====================================================================== #

    def _find_node(self, data):
        """
        Loop throw the hole graph!, to check if a node hase the same
        attributes as the data argument, if so return the node id,
        otherwise return none.
        """
        for node_id, attributes in self.G.nodes(data=True):
            # print(">> {} | {}".format(node_id, attributes))
            if data == attributes:
                # print("data == attributes")
                return node_id
            else:
                pass
                # print("data <> attributes")
        return None
    # ====================================================================== #

    def _invoke_ranges(self, signal, value):
        """get the range value from the corret signal"""
        value = str(value).lower()
        if signal == "fuel_level":
            return self._get_range_key(value, self.settings.FUEL_EFFICIENCY)
        elif signal == "transmission_gear_position":
            return self._get_range_key(value, self.settings.GEAR_POSITION)
        elif signal == "vehicle_speed":
            return self._get_range_key(value, self.settings.VEHICLE_SPEED)
        elif signal == "engine_speed":
            return self._get_range_key(value, self.settings.ENGINE_SPEED)
        elif signal == "torque_at_transmission":
            return self._get_range_key(value, self.settings.TORQUE)
        # elif signal == "accelerator_pedal_position":
        #     return self._get_range_key(value, self.settings.ACCEL_PEDAL)
        # elif signal == "steering_wheel_angle":
        #     return self._get_range_key(value, self.settings.STEERING)
        # elif signal == "brake_pedal_status":
        #     return self._get_range_key(value, self.settings.PARKING_BRAKE)
        else:
            # print("""
            #     Error: The signal <<{}>> is not included in the algorithm!\n
            #     Please take a look at the _INVOKE_RANGES function to add it\n
            #     [line 112].
            # """.format(signal))
            return None
    # ====================================================================== #

    def _get_range_key(self, value, d):
        """retrun the key from the settings list"""
        try:
            value = round(float(value), 2)
            debug_key = ""
            for key in d:
                if d[key][0] <= value <= d[key][1]:
                    # print("V({}) =>".format(key), end=' ')
                    return key
                debug_key = key
            print("404: {} Not Found for {}!!".format(value, d[debug_key]))
            return -99
        except:
            for key in d:
                if d[key] == value:
                    # print("G({}) ====>".format(key), end=' ')
                    return key
            print("Warning: value {} Not Found in any range !".format(value))
            return -99
    # ====================================================================== #

    def _ranges2real(self, signal, value):
        """get the real value from signal range """
        value = int(value)
        if value == 0:
            return 0
        if signal == "fuel_level":
            return json.dumps(self.settings.FUEL_EFFICIENCY[value])
        elif signal == "transmission_gear_position":
            return json.dumps(self.settings.GEAR_POSITION[value])
        elif signal == "vehicle_speed":
            return json.dumps(self.settings.VEHICLE_SPEED[value])
        elif signal == "engine_speed":
            return json.dumps(self.settings.ENGINE_SPEED[value])
        elif signal == "torque_at_transmission":
            return json.dumps(self.settings.TORQUE[value])
        elif signal == "accelerator_pedal_position":
            return json.dumps(self.settings.ACCEL_PEDAL[value])
        elif signal == "steering_wheel_angle":
            return json.dumps(self.settings.STEERING[value])
        elif signal == "brake_pedal_status":
            return json.dumps(self.settings.PARKING_BRAKE[value])
        else:
            return None
    # ====================================================================== #

    def factorize_graph(self, factor=1):
        """Show DriverGraph attributes"""
        try:
            for node_id, attributes in self.G.nodes(data=True):
                for name, value in attributes.items():
                    self.G.node[node_id][name] = float(value) * factor
            for id1, id2 in self.G.edges():
                self.G[id1][id2]['weight'] *= factor
        except ValueError as e:
            print("Errror: ", e)
    # ====================================================================== #

    def export_graphml(self, filename=None):
        """Export the DriverGraph to graphML format"""
        if filename is not None:
            nx.write_graphml(self.G, "{}.graphml".format(filename))

    def import_graphml(self, filename=None):
        """Import the DriverGraph from a graphML file"""
        if filename is not None:
            self.G = nx.read_graphml(filename)
    # ====================================================================== #

    def export_json(self, filename=None):
        """Export the DriverGraph to Json format"""
        if filename is not None:
            g_json = json_graph.node_link_data(self.G)
            json.dump(g_json, open("{}.json".format(filename), 'w'), indent=4)

    def import_json(self, filename=None):
        """Import the DriverGraph from a Json file"""
        if filename is not None:
            with open(filename) as f:
                js_graph = json.load(f)
            self.G = json_graph.node_link_graph(js_graph)
    # ====================================================================== #

    def export_gexf(self, filename=None):
        """Export the DriverGraph to GEXF format"""
        if filename is not None:
            nx.write_gexf(self.G, "{}.gexf".format(filename))
            print("File exported")

    def import_gexf(self, filename=None):
        """Import the DriverGraph from a GEXF file"""
        if filename is not None:
            self.G = nx.read_gexf(filename)
    # ====================================================================== #

    def export_gxl(self, filename=None):
        """Export the DriverGraph to GXL format"""
        if filename is not None:
            write_dot(self.G, "helpers/_tmp/xfile.dot")
            os.system("dot2gxl helpers/_tmp/xfile.dot -o {}".format(filename))
            os.system("sed -i -e '/name=\"name\"/ ,+2d' {}".format(filename))

    def import_gxl(self, filename=None, digraph=True):
        """Import the DriverGraph from a GXL file"""
        if filename is not None:
            os.system("gxl2dot {} -o helpers/_tmp/ifile.dot".format(filename))
            self.G = read_dot("helpers/_tmp/ifile.dot")
    # ====================================================================== #

    def browse_sigma(self, filename=None):
        """View the Graph in borwser using sigmajs and GEXF format"""
        self.export_gexf("helpers/sigma/driver_graph")
        os.system("cd helpers/sigma && python2 -m SimpleHTTPServer 8002")
    # ====================================================================== #

    def vis_network(self, physics=False):
        nodes = []
        for node_id, attributes in self.G.nodes(data=True):
            tmp = {'id': node_id, 'label': node_id, 'color': choice(COLORS)}
            tmp['title'] = "<pre>{}</pre>".format(yaml.dump(
                {k: self._ranges2real(k, v) for k, v in attributes.items()},
                default_flow_style=False
            ))
            nodes.append(tmp)
        edges = []
        for id1, id2 in self.G.edges():
            tmp = {
                'from': id1,
                'to': id2,
                'color': choice(COLORS)
            }
            try:
                tmp['label'] = self.G[id1][id2]['weight']
            except:
                tmp['label'] = self.G[id1][id2][0]['weight']
            edges.append(tmp)
        return {
            "nodes": json.dumps(nodes),
            "edges": json.dumps(edges),
            "physics": json.dumps(physics),
        }
    # ====================================================================== #

    @staticmethod
    def build_multiple(files=None, max_nodes=None, export=False):
        if type(files) is list:
            graphs = []
            for file in files:
                graph = DriverGraph(max_nodes=max_nodes, name="file")
                graph.create_digraph(filename=file)
                graphs.append(graph)
                if export is True:
                    filename = os.path.splitext(os.path.basename(file))[0]
                    graph.export_gxl("{}.gxl".format(filename))
                print("[{}]: {} nodes, edges: {}".format(
                    filename, len(graph.G), len(graph.G.edges())
                ))
            return graphs
        else:
            raise ValueError("Please provide a list of trace files")
    # ====================================================================== #

    @staticmethod
    def divide_graph(G=None, nparts=2):
        if nparts < 1:
            raise ValueError("you cant divide a graph by {}.".format(nparts))
        elif nparts == 1:
            return self.G
        else:
            parts = [[] for i in range(nparts)]
        # print(zip(G, part))
        # for u, i in zip(G, part):
        # G.remove_node(1)
        # graph_size = len(G)
        # print(graph_size)
        # fist_node = [n for n, d in G.in_degree().items() if d == 0]
        # if len(fist_node) != 1:
        #     raise ValueError("The graph has
        # {} root nodes.".format(len(fist_node)))

        # for i in nparts:
        #     print(i * graph_size / nparts)
        #     print(graph_size / nparts)
        #     # for i in range(i * graph_size / nparts, (i + 1) *
        # graph_size / nparts):
        #         # print(i * graph_size / nparts)
        #     # for node_id, attributes in self.G.nodes(data=True):
        #     #     print(i)
        #     pass
        #     # parts[i].append(u)
        #     # return objval, parts
    # ====================================================================== #

    @staticmethod
    def is_isomorphic(G1=None, G2=None, weight=None):
        """
        - Structures that are the same except for relabelling
            (can be the same using relabelling technique)
            are called ISOMORPHIC structures.
        - We can match also nodes attributes & edges attributes
            edge attributes are implemented
        - The function return True if G1 & G2 are isomorphic
            False if not
        """
        if G1 is None or G2 is None:
            raise ValueError("Please provide two graphs.")
        if weight is None:
            return nx.is_isomorphic(G1, G2)
        else:
            em = iso.numerical_edge_match('weight', weight)
            return nx.is_isomorphic(G1, G2, edge_match=em)

# ____________________________ End : DriverGraph ____________________________ #

if __name__ == '__main__':
    try:
        print('working ...')
        Files = [
            # "traces/usa/downtown-west.json",
            # "traces/usa/downtown-west2.json",
            # "traces/usa/uptown-west.json",
            # "traces/usa/uptown-west2.json",
            # "traces/usa/uptown-crossdown.json",
            # "traces/usa/uptown-crosstown.json",
            # "traces/usa/downtown-crosstown.json",
            # "traces/usa/downtown-east.json",
            # "traces/scenarios/localwithgps.json",
            # "traces/scenarios/highway-speeding.json",
        ]
        # graphs = DriverGraph.build_multiple(Files, max_nodes=None, export=True)
        driver = DriverGraph()
        # saya = DriverGraph()
        driver.create_digraph("traces/usa/downtown-crosstown.json")
        driver.export_gxl("downtown-crosstown.gxl")
        print(len(driver.G))
        print(len(driver.G.edges()))
        # driver.import_json("saya.json")
        # saya.import_graphml("saya.graphml")
        # driver.draw_graph('image.png')
        # driver.browse_sigma()
        # driver.export_gxl("graph.gxl")
        driver.factorize_graph(1.5)
        driver.export_gxl("factorized.gxl")
        print("-----")
        print(len(driver.G))
        print(len(driver.G.edges()))
        # print(len(driver.G))
        # print(len(driver.G.edges()))
        # driver.vis_network(True)
        # driver.export_gxl("graph.gxl")
        # if DriverGraph.is_isomorphic(driver.G, saya.G):
        #     print("G1 & G2 are ISOMORPHIC")
        # else:
        #     print("G1 & G2 are NOT isomorphic")
        # driver.export_graphml('saya')
        # driver.export_json('saya')
        # driver.show_attributes()
        #
        # driver.graph_summary()
        # print('---------------')
        # driver.divide_graph(driver.G, 4)
        # print('---------------')
        # driver.graph_summary()
    except ValueError as e:
        print(e)
    # except:
    #     print("Error !!")

    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #
    #

    # print("{} : {}".format(temp.get('name'), temp.get('value')))
    # print('***********************')

    # print('----')
    # print("nam# print(item)
    # print('----')e: {} | value: {}".format(
    # x.get('name', 'NAME'), x.get('value', 'VALUE')))
    # while True:
    #     try:
    #         parser = ijsonself. (line)
    #         for prefix, event, value in parser:
    #             if prefix == "name":
    #                 print(value)
    #             if prefix == "value":
    #                 print(value)
    #             if prefix == "timestamp":
    #                 print(value)
    #     except ValueError:
    #         line += next(f)

    # print("prefix: {} | value: {} | event: {}".format(prefix, value, event))
    # ret = {'builders': {}}
    #     if (prefix, event) == ('builders', 'map_key'):
    #         buildername = value
    #         ret['builders'][buildername] = {}
    #     elif prefix.endswith('.shortname'):
    #         ret['builders'][buildername]['shortname'] = value
    #
    # return ret

    # driver.create_digraph("traces/downtown-crosstown.json")
    # except Exception as e:
    #     print('>> {}'.format(e))

    #
    # data_write_file = sys.argv[2]
    # data_read_file = open(sys.argv[1])
