import plotly.graph_objects as go
import networkx as nx
from pathlib import Path
import os
import subprocess
import importlib.util
import copy

"""
This file handles the logic when a button is pressed on our GUI
__author__ Cade Tipton
__author__ Gatlin Cruz
__author__ Noah Lowry
__author__ Miles Stanley
__version__ 11/10/2021
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
    This setups up the graph based on the parameters from the user and makes an HTML file of the graph
    args:
     hosts: The number of hosts in the graph
     switches: The number of switches in the graph
     controllers: The number of controllers in the graph
     links: The links in the graph
    """
    # The graph object used to build the network throughout the function
    nx_graph = nx.Graph()

    link_list = []
    for link in graph.get('links'):
        link_list.append(link.to_tuple())

    nx_graph.add_edges_from(link_list)

    # Adds a node for each number of host, switch and controller
    for switch in graph.get('switches'):
        nx_graph.add_node(switch.name, type='Switch', color='green', name=switch.name, ip="")
        print("Added switch " + switch.name)
    for controller in graph.get('controllers'):
        nx_graph.add_node(controller.name, type='Controller', color='blue', name=controller.name, ip="")
        print("Added controller " + controller.name)
    for host in graph.get('hosts'):
        nx_graph.add_node(host.name, type='Host', color='red', name=host.name, ip=host.ip)
        print("Added host " + host.name)

    node_x = []
    node_y = []

    # Using NetworkX's Kamada Kawai layout to generate positions for graph nodes. 
    # For more information on how this works, look into Force directed graphs.
    position_dict = nx.kamada_kawai_layout(nx_graph, weight = None)
    for node, position in position_dict.items():
        nx_graph.nodes[node]['pos'] = position

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

    node_text = []
    node_color = []
    # node_size = []
    for node in nx_graph.nodes():
        if nx_graph.nodes[node]['ip'] != "":
            node_text.append(nx_graph.nodes[node]['name'] + " | " + nx_graph.nodes[node]['ip'])  # type
        else:
            node_text.append((nx_graph.nodes[node]['name']))
        node_color.append(nx_graph.nodes[node]['color'])
        # node_size.append(len(nx_graph.nodes[node]['name']) * 25)
    node_trace.marker.color = node_color
    # node_trace.marker.size = node_size
    node_trace.text = node_text
    # node_trace.textfont = dict(
    #     family="monospace",
    #     size=32,
    #     color="red"
    # )

    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False, hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False))
                    )

    fig.write_html(PATH + 'figure.html')


def reset_graph(graph):
    """
    Resets the values of the graph to empty lists
    args:
      graph: The graph list being used
    """
    for key in graph.keys():
        graph[key].clear()


def clear_output(extra):
    """
    Resets the values of the output to empty lists
    args:
      extra: The extra list being used
    """
    for key in extra.keys():
        extra[key] = ""


def make_file(graph):
    """
    Creates a Python file that represents a network using Mininet
    args:
       graph: The graph list with the values for the network
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
        # for link in graph.get('links'):
        #     if host.name == link.first or host.name == link.second:
        new_file.write(host.add_ip_to_file())


def get_mininet_file():
    path = str(Path.home()) + "/Desktop/"
    return open(path + "new_file.py", "a")

# Measures latency
def add_ping_all():
    """
    Method to test the latency for all nodes.
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
    args:
       extra: The holder for the results to be stored to
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

    # errors = errors.replace("[sudo] password for Gatlin: ", "")
    errors = errors.replace("[sudo] password for mininet: ", "")

    extra['ping'] = errors


def add_to_database(graph, graph_name):
    bolt_url = "neo4j://localhost:7687"
    # The default username for Neo4j
    user = "neo4j"
    # The password we use to gain access to the database
    password = "mininet"
    # Creating an app object from the db_testing file
    app = db_testing.App(bolt_url, user, password)

    for host in graph.get('hosts'):
        app.create_node(host.name, graph_name, 'host', host.ip)
    for switch in graph.get('switches'):
        app.create_node(switch.name, graph_name, 'switch')
    for controller in graph.get('controllers'):
        app.create_node(controller.name, graph_name, 'controller')
    for link in graph.get('links'):
        print(app.create_links_db(link.first, link.second, graph_name).peek())

    app.create_csv(graph_name)

    app.close()


def save_database():
    bolt_url = "neo4j://localhost:7687"
    # The default username for Neo4j
    user = "neo4j"
    # The password we use to gain access to the database
    password = "mininet"
    # Creating an app object from the db_testing file
    app = db_testing.App(bolt_url, user, password)
    temp = app.test1()
    print(temp.values())

def remove_host(node, graph):
    """
    This method removes a node from the graph by checking for equivilant attributes within a list
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
    """
    for link in graph['links']:
        if ((link.first == first_name) or (link.first == second_name)) and ((link.second == first_name) or (link.second == second_name)):
            graph['links'].remove(link)
            print("Link between " + first_name + " and " + second_name + " removed")
            return

def remove_assoc_links(node, graph):
    """
    This method removes any links associated with a node
    """
    # if(node.get('name') == "hr1"):
    #     print("Printing links remaining")
    #     print(graph['links'])
    for link in copy.deepcopy(graph['links']):
        print("Comparing " + node.get('name') + " to " + link.first + " and " + link.second)
        if ((link.first == node.get('name')) or (link.second == node.get('name'))):
            # error here
            # graph['links'].remove(link)

            # Is there a more efficient solution?
            remove_links(link.first, link.second, graph)

            # print("Link between " + link.first + " and " + link.second + " removed")
    return

def main():
    """
    The main method that creates a path
    """
    # custom_path = "/home/mininet/mininet/custom/"

    # base_file = open(custom_path + "base_file.py", "a")
    #
    # host_text = ""
    # switch_text = ""
    # for host in range(4):  # graph.get('num_hosts')
    #     host_text += "\th" + str(host + 1) + " = self.addHost( 'h" + str(host + 1) + "' )\n"
    # for switch in range(2):  # graph.get('num_switches')
    #     switch_text += "\ts" + str(switch + 1) + " = self.addSwitch( 's" + str(switch + 1) + "' )\n"
    #
    # print(host_text)
    # print(switch_text)
    #
    # base_file.write("\t#Add hosts\n" + host_text + "\n")
    # base_file.write("\t#Add switches\n" + switch_text)
    # other_path = "/home/mininet/Desktop/"
    # make_file()

    # run_mininet(other_path)


if __name__ == '__main__':
    main()
