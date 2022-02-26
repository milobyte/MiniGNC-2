import plotly.graph_objects as go
import networkx as nx
from pathlib import Path
import os
import subprocess
import importlib.util
import copy

"""
This file handles the logic when a button is pressed on our GUI
__author__: Gatlin Cruz
__author__: Cade Tipton
__author__: Noah Lowry
__author__: Miles Stanley
__version__: 12/2/21
"""
BASE_DIR = Path(__file__).resolve().parent.parent
PATH = os.path.join(BASE_DIR, "gui/")

# For Windows
"""This is the path we use when running on a windows machine"""
# spec = importlib.util.spec_from_file_location("buttons", str(BASE_DIR) + "\\gui\\templates\\gui\\buttons.py")

# For Mac
"""This is the path we use when running on a mac/linux machine"""
spec = importlib.util.spec_from_file_location("db_testing", str(BASE_DIR) + "/db_testing.py")

db_testing = importlib.util.module_from_spec(spec)
spec.loader.exec_module(db_testing)

filename = ''


def make_graph(graph):
    """
    This sets up the graph based on the parameters from the user and makes an HTML file of the graph
    :param graph: The object that stores the different nodes and links within the network

    Author: Orignally Written by Gatlin and Cade. Modified by Noah and Miles (roughly 60% was modified)
    """
    # The graph object used to build the network throughout the function
    nx_graph = nx.Graph()

    # Adds links from within the network
    link_list = []
    for link in graph.get('links'):
        link_list.append(link.to_tuple())

    # Sets edges for nx_graph
    nx_graph.add_edges_from(link_list)

    # Setting the nodes and positions for nx_graph
    set_nx_graph_nodes(graph, nx_graph)

    # Setting node_trace and edge_trace for Plotly graphing
    node_trace = get_node_trace(nx_graph)
    edge_trace = get_edge_trace(nx_graph)

    # Setting the text to display on node hover
    set_node_text(nx_graph, node_trace)

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False, hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    fig.write_html(PATH + 'figure.html')

def set_nx_graph_nodes(graph, nx_graph):
    """
    This function sets up the different nodes for the nx_graph object used to graph the network.

    :param graph: The object that stores the different nodes and links within the network
    :param nx_graph: The object used to represent the network

    Author: Orignally Written by Gatlin and Cade. Modified by Noah and Miles (roughly 70% was modified for position plotting)
    """
    # Adds a node for each number of host, switch and controller
    for switch in graph.get('switches'):
        nx_graph.add_node(switch.name, type='Switch', color='green', name=switch.name, ip="")
        # print("Added switch " + switch.name)
    for controller in graph.get('controllers'):
        nx_graph.add_node(controller.name, type='Controller', color='blue', name=controller.name, ip="")
        # print("Added controller " + controller.name)
    for host in graph.get('hosts'):
        nx_graph.add_node(host.name, type='Host', color='red', name=host.name, ip=host.ip, links_info=host.link_log)
        # print("Added host " + host.name)

    # Using NetworkX's Kamada Kawai layout to generate positions for graph nodes. 
    # For more information on how this works, look into Force directed graphs.
    position_dict = nx.kamada_kawai_layout(nx_graph, weight = None)
    for node, position in position_dict.items():
        nx_graph.nodes[node]['pos'] = position


def get_node_trace(nx_graph):
    """
    This function sets up the object that will determine how nodes are graphed.
    :param nx_graph: The object used to represent the network

    :return node_trace: the object that allows Plotly to graph the nodes of the network

    Author: Orignally Written by Gatlin and Cade. Modified by Noah and Miles (roughly 40% was modified for position plotting)
    """
    node_x = []
    node_y = []

    # Assigns positions to node_x and node_y lists
    for node in nx_graph.nodes():
    
        x, y = nx_graph.nodes[node]['pos']
        node_x.append(x)
        node_y.append(y)

    # Graphs the nodes based on the positions provided and other parameters
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers',
        hoverinfo='text',
        marker=dict(
            size=10,
            color=[],
            opacity=1.0,
            line=dict(
                color='black',
                width=2
            )
        ),
        hoverlabel=dict(
            bgcolor="white",
            font_size=24,
            font_family="monospace",
        ),
    )

    return node_trace

def get_edge_trace(nx_graph):
    """
    This function sets up the object used to graph the edges of the network.
    :param nx_graph: The object used to represent the network

    :return edge_trace: the object that allows Plotly to graph the edges of the network

    Author: Orignally Written by Gatlin and Cade. Modified by Noah and Miles (roughly 5% was modified for position plotting)
    """
    # Declaring and defining edges within the network
    edge_x = []
    edge_y = []
    for edge in nx_graph.edges():
        x0, y0 = nx_graph.nodes[edge[0]]['pos']
        x1, y1 = nx_graph.nodes[edge[1]]['pos']
        edge_x.append(x0)
        edge_x.append(x1)
        edge_x.append(None)
        edge_y.append(y0)
        edge_y.append(y1)
        edge_y.append(None)

    # Graphing the edges
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=.5, color='black'),
        hoverinfo='none',
        mode='lines')

    return edge_trace

def set_node_text(nx_graph, node_trace):
    """
    This function sets up text that will be displayed upon hovering over a node within the graph.
    :param nx_graph: The object used to represent the network
    :param node_trace: the object that allows Plotly to graph the nodes of the network

    Author: Orignally Written by Gatlin and Cade. Modified by Noah and Miles (roughly 20% was modified for position plotting)
    """
    # Determines the text to display for identifying nodes on the graph
    node_text = []
    node_color = []
    for node in nx_graph.nodes():
        if nx_graph.nodes[node]['ip'] != "":
            node_text.append(nx_graph.nodes[node]['name'] + " | " + nx_graph.nodes[node]['ip'] + "<br>" + 
            nx_graph.nodes[node]['links_info'][0] + "<br>" + nx_graph.nodes[node]['links_info'][1])  # use <br> for new lines
        else:
            node_text.append((nx_graph.nodes[node]['name']))
        node_color.append(nx_graph.nodes[node]['color'])
    node_trace.marker.color = node_color
    node_trace.text = node_text


def reset_graph(graph):
    """
    Resets the values of the graph to empty lists
    :param graph: The graph list being used
    """
    for key in graph.keys():
        graph[key].clear()


def clear_output(extra):
    """
    Resets the values of the output to empty lists
    :param extra: The extra list being used
    """
    for key in extra.keys():
        extra[key] = ""


def make_file(graph):
    """
    Creates a Python file that represents a network using Mininet
    :param graph: The graph list with the values for the network

    Author: Written by Cade and Gatlin. Modified by Miles and Noah (10%)
    """

    path = str(Path.home()) + "/Desktop/"
    new_file = open(path + "new_file.py", "w+")
    # Writing the initial imports needed for our Mininet functions to work
    new_file.write("from mininet.net import Mininet\nfrom mininet.cli import CLI\n"
                   "from mininet.link import TCLink\nnet = Mininet(link=TCLink)\n")

    # By key, navigate through the network and write the Mininet code needed to new_file.py
    for key in graph.keys():
        for node in graph.get(key):
            new_file.write(node.add_to_file())
        new_file.write("\n")

    # Sets IP within Mininet for each host
    for host in graph.get('hosts'):
        new_file.write(host.add_ip_to_file())


def get_mininet_file():
    """
    Returns a reference to the new file used to run Mininet commands
    """
    path = str(Path.home()) + "/Desktop/"
    return open(path + "new_file.py", "a")

# Measures latency
def add_ping(host1, host2):
    """
    Method to test the latency between two hosts.
    Author: Miles and Noah
    """
    new_file = get_mininet_file()
    new_file.write("\nnet.start()\nnet.ping([" + host1 + ", " + host2 + "])\nnet.stop()\n")

# Measures latency
def add_ping_all():
    """
    Method to test the latency for all nodes.
    Author: Miles and Noah
    """
    new_file = get_mininet_file()
    new_file.write("\nnet.start()\nnet.pingAll()\nnet.stop()\n")

# Measures throughput
def add_iperf(host1, host2):
    """
    Method to test the throughput between two hosts.
    """
    new_file = get_mininet_file()
    new_file.write("\nnet.start()\nnet.iperf([" + host1 + ", " + host2 + "])\nnet.stop()\n")


def run_mininet(extra):
    """
    Method to run Mininet in the background so the user can run commands through it
    :param extra: The holder for the results to be stored to
    :return: None
    """

    path = str(Path.home()) + "/Desktop/"

    sudo_pw = "Mininet"
    command = "python2 " + path + "new_file.py"
    command = command.split()

    cmd1 = subprocess.Popen(['echo', sudo_pw], stdout=subprocess.PIPE)
    cmd2 = subprocess.Popen(['sudo', '-S'] + command, stdin=cmd1.stdout,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    outs, errors = cmd2.communicate()
    print("outs" + outs + "\nerrors: " + errors + "end")

    # REPLACE USERNAME WITH CURRENT USERNAME IF NEEDED
    errors = errors.replace("[sudo] password for milobyte: ", "")

    # print("\nAdding '" + errors + "' to output!\n")
    extra['ping'] = errors

    # Returning text to add to respective hosts' link logs
    return errors


def add_to_database(graph, graph_name):
    """
    Creates a CSV file representing the network using Neo4j
    :param graph: The graph list with the values for the network
    :param graph_name: The name of the graph
    :return: None
    """
    bolt_url = "neo4j://localhost:7687"
    # The default username for Neo4j
    user = "neo4j"
    # The password we use to gain access to the database
    password = "mininet"
    # Creating an app object from the db_testing file
    app = db_testing.App(bolt_url, user, password, graph_name)

    for host in graph.get('hosts'):
        app.create_node(host.name, graph_name, host.type, host.ip, host.get_iperf_log(), host.get_ping_log(), graph_name)
    for switch in graph.get('switches'):
        app.create_node(switch.name, graph_name, switch.type, db = graph_name)
    for controller in graph.get('controllers'):
        app.create_node(controller.name, graph_name, controller.type, db = graph_name)
    for link in graph.get('links'):
        print(app.create_links_db(link.get_first(), link.get_second(), graph_name, link.get_bandwidth(), 
            link.get_delay(), link.get_loss(), link.get_queue_size(), db = graph_name).peek())

    app.create_csv(graph_name)

    app.close()


# def save_database():
#     bolt_url = "neo4j://localhost:7687"
#     # The default username for Neo4j
#     user = "neo4j"
#     # The password we use to gain access to the database
#     password = "mininet"
#     # Creating an app object from the db_testing file
#     app = db_testing.App(bolt_url, user, password)
#     temp = app.test1()
#     print(temp.values())

def clear_database(db = "neo4j"):
    bolt_url = "neo4j://localhost:7687"
    # The default username for Neo4j
    user = "neo4j"
    # The password we use to gain access to the database
    password = "mininet"
    # Creating an app object from the db_testing file
    app = db_testing.App(bolt_url, user, password)
    result = app.clear_data(db)
    app.close()
    return result

def remove_host(node, graph):
    """
    This method removes a node from the graph by checking for equivilant attributes within a list
    Author: Miles and Noah
    """
    for host in graph['hosts']:
        if host.get_name() == node.get('name'):
            graph['hosts'].remove(host)
            print(str(host.get_name()) + " removed")
            remove_assoc_links(node, graph)
            return

def remove_switch(node, graph):
    """
    This method removes a node from the graph by checking for equivilant attributes within a list
    Author: Noah and Miles
    """
    for switch in graph['switches']:
        if switch.get_name() == node.get('name'):
            graph['switches'].remove(switch)
            print(str(switch.get_name()) + " removed")
            remove_assoc_links(node, graph)
            return

def remove_controller(node, graph):
    """
    This method removes a node from the graph by checking for equivilant attributes within a list
    Author: Miles and Noah
    """
    for controller in graph['controllers']:
        if controller.get_name() == node.get('name'):
            graph['controllers'].remove(controller)
            print(str(controller.get_name()) + " removed")
            remove_assoc_links(node, graph)
            return

def remove_links(first_name, second_name, graph):
    """
    This method removes a node from the graph by checking for equivilant attributes within a list
    Author: Miles and Noah
    """
    for link in graph['links']:
        if ((link.first == first_name) or (link.first == second_name)) and ((link.second == first_name) or (link.second == second_name)):
            graph['links'].remove(link)
            print("Link between " + first_name + " and " + second_name + " removed")
            return

def remove_assoc_links(node, graph):
    """
    This method removes any links associated with a node
    Author: Miles and Noah
    """
    for link in copy.deepcopy(graph['links']):
        print("Comparing " + node.get('name') + " to " + link.first + " and " + link.second)
        if ((link.first == node.get('name')) or (link.second == node.get('name'))):
            remove_links(link.first, link.second, graph)

    return

if __name__ == '__main__':
    main()
