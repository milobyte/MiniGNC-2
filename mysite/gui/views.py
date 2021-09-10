import importlib.util

from django.shortcuts import render
from pathlib import Path
from . import nodes
import csv

"""
This files is a generated file from Django that we use
to receive feedback from the GUI
__author__: Gatlin Cruz
__author__: Cade Tipton
__version__: 9/15/20
"""

BASE_DIR = Path(__file__).resolve().parent.parent

# For Windows
"""This is the path we use when running on a windows machine"""
# spec = importlib.util.spec_from_file_location("buttons", str(BASE_DIR) + "\\gui\\templates\\gui\\buttons.py")

# For Mac
"""This is the path we use when running on a mac/linux machine"""
spec = importlib.util.spec_from_file_location("buttons", str(BASE_DIR) + "/gui/templates/gui/buttons.py")

buttons = importlib.util.module_from_spec(spec)
spec.loader.exec_module(buttons)

"""This graph nodes is linked to the HTML doc for our GUI. The values are stored in this dict"""
graph_nodes = {
    'hosts': [],
    'switches': [],
    'controllers': [],
    'links': []
}

"""This is the extra text used to display the ping results from Mininet"""
extra_text = {
    'ping': ""
}

"""This is how Django connects the lists to the HTML"""
context = {
    'graph': graph_nodes,
    'output': extra_text,
}


def home(request):
    """
    This is the main method for our GUI. It checks if any of the buttons have been pressed
    and does the appropriate method call. It also sets the parameters for the graph when the 
    user hits the set button
    return: The GUI html to display to the user
    """
    # This is the logic for when the set button is clicked
    if request.GET.get('setbtn'):
        print(graph_nodes)
        buttons.make_file(graph_nodes, True)

    # This is the logic for when the add host button is clicked
    elif request.GET.get('add_host_btn'):
        name = request.GET.get('add_host_name')
        ip = request.GET.get('add_host_ip')
        host = nodes.Host(name, ip)
        graph_nodes['hosts'].append(host)

    # This is the logic for when the add switch button is clicked
    elif request.GET.get('add_switch_btn'):
        name = request.GET.get('add_switch_name')
        switch = nodes.Switch(name)
        graph_nodes['switches'].append(switch)

    # This is the logic for when the add controller button is clicked
    elif request.GET.get('add_controller_btn'):
        name = request.GET.get('add_controller_name')
        controller = nodes.Controller(name)
        graph_nodes['controllers'].append(controller)

    # This is the logic for when the add link button is clicked
    elif request.GET.get('add_link_btn'):
        first = request.GET.get('add_first_link')
        second = request.GET.get('add_second_link')
        link = nodes.Link(first, second)
        graph_nodes['links'].append(link)

    # This is the logic for when the graph button is clicked
    elif request.GET.get('graphbtn'):
        buttons.make_graph(graph_nodes)
        return render(request, 'gui/figure.html', context)

    # This is the logic for when the reset button is clicked
    elif request.GET.get('resetbtn'):
        buttons.reset_graph(graph_nodes)

    elif request.GET.get('clearoutputbtn'):
        buttons.clear_output(extra_text)

    # This is the logic for when the ping button is clicked
    elif request.GET.get('pingbtn'):
        buttons.make_file(graph_nodes)
        buttons.add_ping_all()
        buttons.run_mininet(extra_text)

    # This is the logic for when the add_data button is clicked
    elif request.GET.get('add_databtn'):
        filename = request.GET.get('save_file_name')
        buttons.add_to_database(graph_nodes, filename)

    # This is the logic for when the load_data button is clicked
    elif request.GET.get('load_databtn'):
        file = request.GET.get('load_databtn')
        path = str(Path.home()) + "/Desktop/" + file
        full_list = []

        with open(path, newline='') as csv_file:
            csv_r = csv.DictReader(csv_file)

            for row in csv_r:
                full_list.append(row)
                if row['_labels'] == ":" + file.replace(".csv", ""):
                    if row['type'] == 'host':
                        graph_nodes['hosts'].append(nodes.Host(row.get('name'), row.get('ip')))
                    elif row['type'] == 'switch':
                        graph_nodes['switches'].append(nodes.Switch(row.get('name')))
                    elif row['type'] == 'controller':
                        graph_nodes['controllers'].append(nodes.Controller(row.get('name')))

                if row['_start'] != "":
                    first_index = row.get('_start')
                    second_index = row.get('_end')
                    for item in full_list:
                        if item.get('_id') == first_index:
                            first = item.get('name')
                    for item in full_list:
                        if item.get('_id') == second_index:
                            second = item.get('name')
                    graph_nodes['links'].append(nodes.Link(first, second))

    elif request.GET.get('iperf_btn'):
        host1 = request.GET.get('iperf_host1_name')
        host2 = request.GET.get('iperf_host2_name')

        buttons.make_file(graph_nodes)
        buttons.add_iperf(host1, host2)
        buttons.run_mininet(extra_text)

    return render(request, 'gui/gui.html', context)


def graph(request):
    """
    This method creates the graph HTML and displays to the user
    return: The rendered HTML of the graph
    """
    return render(request, 'gui/figure.html')
