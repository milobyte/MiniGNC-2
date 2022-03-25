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
__author__: Noah Lowry
__author__: Miles Stanley
__version__: 12/2/21
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
    author: Originally written by Cade Tipton and Gatlin Cruz
    author: 80% Modified by Noah Lowry and Miles Stanley
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
        bandwidth = request.GET.get('add_bandwidth')
        delay = request.GET.get('add_delay')
        loss = request.GET.get('add_loss')
        queue_size = request.GET.get('add_queue_size')
        link = nodes.Link(first, second)
        if bandwidth != 'default' and bandwidth.isdigit():
            link.set_bandwidth(bandwidth)
        if delay != 'default' and ((delay[-2:]) == 'ms') and (delay[:-2].isdigit()):
            link.set_delay(delay)
        if loss != 'default' and loss.isdigit():
            link.set_loss(loss)
        if queue_size != 'default' and queue_size.isdigit():
            link.set_queue_size(queue_size)

        graph_nodes['links'].append(link)

    # This is the logic for when the graph button is clicked
    elif request.GET.get('graphbtn'):
        try:
            buttons.make_graph(graph_nodes)
            return render(request, 'gui/figure.html', context)
        except:
            extra_text['ping'] = "Error: Graph Generation cannot be completed. Make sure no faulty links exist within the network."

    # This is the logic for when the reset button is clicked
    elif request.GET.get('resetbtn'):
        buttons.reset_graph(graph_nodes)

    elif request.GET.get('clearoutputbtn'):
        buttons.clear_output(extra_text)

    # This is the logic for when the ping button is clicked
    elif request.GET.get('pingallbtn'):
        buttons.make_file(graph_nodes)
        buttons.add_ping_all()
        buttons.run_mininet(extra_text)

    # This is the logic for when the add_data button is clicked
    elif request.GET.get('add_databtn'):
        filename = request.GET.get('save_file_name')
        buttons.add_to_database(graph_nodes, filename)

    # This is the logic for when the run_single_query button is clicked
    elif request.GET.get('single_query_databtn'):
        conditional = request.GET.get('single_select')
        network_name = request.GET.get('network_name')
        
        if "BW" in conditional:
            results = buttons.run_bw_query(conditional, network_name)
        elif "LS" in conditional:
            results = buttons.run_ls_query(conditional, network_name)
        elif "DY" in conditional:
            results = buttons.run_dy_query(conditional, network_name)
        elif "QU" in conditional:
            results = buttons.run_qu_query(conditional, network_name)

        result_str = ""
        for record in enumerate(results):
            result_str += (record[1].value(0) + " -> " + record[1].value(1) + "\n")

        extra_text['ping'] = result_str

    # This is the logic for when the clear database button is clicked
    elif request.GET.get('clr_database'):
        db_name = request.GET.get('clear_file_name')
        result = buttons.clear_database(db_name)
        extra_text['ping'] = "Database has been cleared."


    # This is the logic for when the load_data button is clicked
    elif request.GET.get('load_databtn'):
        file = request.GET.get('load_databtn')
        path = str(Path.home()) + "/Desktop/" + file
        full_list = []

        with open(path, newline='') as csv_file:
            csv_r = csv.DictReader(csv_file)

            for row in csv_r:
                full_list.append(row)
                # if row['_labels'] == ":" + file.replace(".csv", ""):
                if row['_labels'] != "":
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
                    link = nodes.Link(first, second)
                    set_link_params(link, row)
                    graph_nodes['links'].append(link)

    #  This is the logic for when the remove_data button is clicked
    elif request.GET.get('remove_databtn'):
        file = request.GET.get('remove_databtn')
        path = str(Path.home()) + "/Desktop/" + file
        full_list = []

        with open(path, newline='') as csv_file:
            csv_r = csv.DictReader(csv_file)

            for row in csv_r:
                #removing nodes based on type                
                if row['_labels'] != "":
                    if row['type'] == 'host':
                        buttons.remove_host(row, graph_nodes)
                    elif row['type'] == 'switch':
                        buttons.remove_switch(row, graph_nodes)
                    elif row['type'] == 'controller':
                        buttons.remove_controller(row, graph_nodes)
                #removing links specified in csv file
                if row['_start'] != "":
                    first_name = row.get('_start')
                    second_name = row.get('_end')
                    buttons.remove_links(first_name, second_name, graph_nodes)
            
            print(graph_nodes)

    #Logic for when the iPerf button is clicked for testing bandwidth
    elif request.GET.get('iperf_btn'):
        host1 = request.GET.get('iperf_host1_name')
        host2 = request.GET.get('iperf_host2_name')

        host_bundle = get_hosts(host1, host2)
        if host_bundle != None: #If both hosts exist
            if (check_link_status(host1, host2)): #If the link between two hosts has no loss
                buttons.make_file(graph_nodes)
                buttons.add_iperf(host1, host2)
                output = buttons.run_mininet(extra_text)
                if "Could not connect to iperf" in output:
                    output = "Iperf Failed"
                    extra_text['ping'] = (output + "\nMake sure there is a path between hosts.\n" +
                        "If Path has Packet Loss, try again until packet makes it through or remove packet loss.")

                add_iperf_info(host_bundle, output)
                
            else:
                extra_text['ping'] = "Error: IPerf not available for links with defined loss!"
        else:
            extra_text['ping'] = "Error: At least one of the hosts provided does not exist!"

    #Logic for when the Ping button is clicked for testing latency
    elif request.GET.get('ping_btn'):
        host1 = request.GET.get('ping_host1_name')
        host2 = request.GET.get('ping_host2_name')

        host_bundle = get_hosts(host1, host2)
        if host_bundle != None: #If both hosts exist
            buttons.make_file(graph_nodes)
            buttons.add_ping(host1, host2)
            output = "***Ping: " + buttons.run_mininet(extra_text)
            add_ping_info(host_bundle, output)
        else:
            extra_text['ping'] = "Error: At least one of the hosts provided does not exist!"

    return render(request, 'gui/gui.html', context)

def add_iperf_info(host_bundle, output):
    """
    Sets the iPerf log for each host to the most recent iPerf output
    author: Noah Lowry and Miles Stanley
    :param host1: The first host involved in the bandwidth test
    :param host2: The second host involved in the bandwidth test
    :param output: The output of the bandwidth test to be set within each host's link log
    :return: None
    """
    print("")
    HOST_1_POS = 0
    HOST_2_POS = 1

    first_host = host_bundle[HOST_1_POS]
    second_host = host_bundle[HOST_2_POS]
    first_host.set_link_log('iperf', output)
    second_host.set_link_log('iperf', output)

def add_ping_info(host_bundle, output):
    """
    Sets the Ping log for each host to the most recent Ping output
    author: Noah Lowry and Miles Stanley
    :param host1: The first host involved in the ping test
    :param host2: The second host involved in the ping test
    :param output: The output of the ping test to be set within each host's link log
    :return: None
    """
    print("")
    HOST_1_POS = 0
    HOST_2_POS = 1

    first_host = host_bundle[HOST_1_POS]
    second_host = host_bundle[HOST_2_POS]
    first_host.set_link_log('ping', output) 
    second_host.set_link_log('ping', output)

def get_hosts(host1, host2):
    """
    Returns an array of host objects based on the name provided. If one of them does 
    not exist within the network, return None
    author: Noah Lowry and Miles Stanley
    :param host1: The first host name
    :param host2: The second host name
    :return: An array containing the two respective Host objects or None
    """
    first_host = get_host(host1)
    second_host = get_host(host2)
    if (first_host == None) or (second_host == None):
        return None
    else:
        return [first_host, second_host]

def check_link_status(host1, host2):
    """
    Method used to ensure the link between two hosts does not have defined loss. Testing bandwidth with
    defined loss leads to error due to packet loss.
    author: Miles Stanley
    :param host1: The first host name
    :param host2: The second host name
    :return: True if the link has no defined loss, False otherwise
    """
    return True #testing-------------------------------------------------------------------------------------DELETE

    for link in graph_nodes['links']:
        if link.get_first() == host1 and link.get_second() == host2:
            if link.get_loss() == None:
                return True
    return False


def get_host(host):
    """
    Gets a host object based on the host name provided
    author: Miles Stanley
    :param host: the host name of the host to return
    :return: the host object with the same name as the parameter provided
    """
    for new_host in graph_nodes['hosts']:
        if new_host.name == host:
            return new_host

def set_link_params(link, row):
    """
    This function searches a row from a CSV file in order to apply any link parameters to a given link
    :param link: The link object to apply any parameters to if necessary
    :param row: The row from our CSV file to determine link parameters based on column

    author: Noah Lowry
    """
    # Following Logic Adds the Network Parameters to each link
    # KeyErrors are ignored, if a column header does not exist, then the parameter is not added
    try:
        if row['_bw'] != "":
            bw_value = row.get('_bw')
            if bw_value.isdigit():
                # print("Added new bandwidth " + bw_value)
                link.set_bandwidth(bw_value)
    
    except KeyError:
        pass

    try:
        if row['_delay'] != "":
            delay_value = row.get('_delay')
            if ((delay_value[-2:]) == 'ms') and (delay_value[:-2].isdigit()):
                # print("Added new delay " + delay_value)
                link.set_delay(delay_value)
    
    except KeyError:
        pass

    try:
        if row['_loss'] != "":
            loss_value = row.get('_loss')
            if loss_value.isdigit():
                # print("Added new loss " + loss_value)
                link.set_loss(loss_value)
    
    except KeyError:
        pass

    try:
        if row['_queue'] != "":
            queue_value = row.get('_queue')
            if queue_value.isdigit():
                # print("Added new queue value " + queue_value)
                link.set_queue_size(queue_value)
    
    except KeyError:
        pass


def graph(request):
    """
    This method creates the graph HTML and displays to the user
    return: The rendered HTML of the graph
    """
    return render(request, 'gui/figure.html')
