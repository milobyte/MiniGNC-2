"""
This file contains classes for nodes in the network
__author__ Cade Tipton
__author__ Gatlin Cruz
__version__ 4/27/21
"""


class Host:
    def __init__(self, name, ip):
        """
        Creates a new Host object
        :param name: The name of the host
        :param ip: The ip of the host
        :return: None
        """
        self.name = name
        self.ip = ip

    def __str__(self):
        """
        Used to display host in a formatted way
        :return: a formatted string
        """
        return self.name + ": ip - " + self.ip

    def __repr__(self):
        """
        Used to display host in a formatted way
        :return: a formatted string
        """
        return self.name + ": ip - " + self.ip

    def add_to_file(self):
        """
        Automates the text to add a host to a file
        :return: the text to add a host to a file
        """
        return self.name + " = net.addHost( '" + self.name + "' )\n"

    def add_ip_to_file(self):
        """
        Automates the text to add host ip to a file
        :return: the text to add a host ip to a file
        """
        return self.name + ".setIP( '" + self.ip + "' )\n"

    def get_ip(self):
        """
        Getter for the ip address
        :return: ip The ip of the host
        """
        return self.ip

    def get_name(self):
        """
        Getter for the name of a host
        :return: name The name of the host
        """
        return self.name


class Switch:
    def __init__(self, name):
        """
        Creates a new Switch object
        :param name: The name of the switch
        :return: None
        """
        self.name = name

    def __str__(self):
        """
        Used to display switch in a formatted way
        :return: a formatted string
        """
        return str(self.name)

    def __repr__(self):
        """
        Used to display switch in a formatted way
        :return: a formatted string
        """
        return str(self.name)

    def add_to_file(self):
        """
        Automates the text to add a switch to a file
        :return: the text to add a switch to a file
        """
        return self.name + " = net.addSwitch( '" + self.name + "' )\n"
    
    def get_name(self):
        """
        Getter for the name of a switch
        :return: name The name of the switch
        """
        return self.name


class Controller:
    def __init__(self, name):
        """
        Creates a Controller object
        :param name: The name of the controller
        :return: None
        """
        self.name = name

    def __str__(self):
        """
        Used to display controller in a formatted way
        :return: a formatted string
        """
        return str(self.name)

    def __repr__(self):
        """
        Used to display controller in a formatted way
        :return: a formatted string
        """
        return str(self.name)

    def add_to_file(self):
        """
        Automates the text to add a controller to a file
        :return: the text to add a controller to a file
        """
        return self.name + " = net.addController( '" + self.name + "' )\n"

    def get_name(self):
        """
        Getter for the name of a controller
        :return: name The name of the controller
        """
        return self.name


class Link:
    def __init__(self, first, second):
        """
        Creates a Link object
        :param first: The first item in the link
        :param second: The second item in the link
        :return: None
        """
        self.first = first
        self.second = second
        self.bandwidth = None
        self.delay = None
        self.loss = None
        self.max_queue_size = None

    def __str__(self):
        """
        Used to display link in a formatted way
        :return: the formatted string
        """
        return self.first + " <-> " + self.second

    def __repr__(self):
        """
        Used to display link in a formatted way
        :return: the formatted string
        """
        return str(self.first) + " <-> " + str(self.second)

    def add_to_file(self):
        """
        Automates the text to add a link to a file
        :return: the text to add a link to a file
        """
        linkOptsString = "link_opts = dict(bw = " + str(self.bandwidth) + ", delay = '" + str(self.delay) + "', loss = " + str(self.loss) + ", max_queue_size = " + str(self.max_queue_size) + ")\n"
        # Use String building? 
        # if self.bandwidth == None: 
        #     return self.first + self.second + " = net.addLink( '" + self.first + "', " + "'" + self.second + "' )\n"
        # elif self.delay == None:
        #     return self.first + self.second + " = net.addLink( '" + self.first + "', " + "'" + self.second + "', bw = " + self.bandwidth + ")\n"
        # else: 
        #     return self.first + self.second + " = net.addLink( '" + self.first + "', " + "'" + self.second + "', bw = " + self.bandwidth + ", delay = '" + self.delay + "' )\n"
        linkInitializer = linkOptsString + self.first + self.second + " = net.addLink( '" + self.first + "', " + "'" + self.second + "', **link_opts )\n"
        return linkInitializer


    def to_tuple(self):
        """
        Converts the first and second item into a tuple
        :return: a tuple containing the first and second item
        """
        return tuple((self.first, self.second))

    def set_bandwidth(self, bandwidth):
        """
        Sets a value to the bandwidth limit of a link (measured in megabits per second)
        :param bandwidth: the Mbps of bandwidth that a link has
        :return: None
        """
        # SET RESTRICTIONS
        print("BANDWIDTH: " + bandwidth + " ADDED")
        self.bandwidth = bandwidth

    def get_bandwidth(self):
        """
        Returns the Mbps of bandwidth set for a link if initialized
        :return: Mbps of bandwidth of a link or None if bandwidth was not initialized
        """
        return self.bandwidth

    def set_delay(self, delay):
        """
        Sets a value to the transmission delay of a link (measured in milliseconds)
        :param delay: the transmission delay a link has (measured in milliseconds)
        :return: None
        """
        # SET RESTRICTIONS
        self.delay = delay
        print("DELAY: " + delay + " ADDED")

    def get_delay(self):
        """
        Returns the value to the transmission delay of a link if initialized
        :return: value to the transmission delay of a link or None if delay was not initialized
        """
        return self.delay

    def set_loss(self, loss):
        """
        Sets a value representing the precentage of loss in packets of a link 
        :param loss: the precentage of loss in packets of a link 
        :return: None
        """
        # SET RESTRICTIONS
        self.loss = loss
        print("LOSS: " + loss + " ADDED")

    def get_loss(self):
        """
        Returns the value representing the precentage of loss in packets of a link 
        :return: representing the precentage of loss in packets of a link  or None if loss was not initialized
        """
        return self.loss

    def set_queue_size(self, size):
        """
        Sets a value to the packet queue size of a link (measured in packet number)
        :param delay: the packet queue size of a link (measured in packet number)
        :return: None
        """
        # SET RESTRICTIONS
        self.max_queue_size = size
        print("MAX QUEUE SIZE: " + size + " ADDED")

    def get_queue_size(self):
        """
        Returns the value to the packet queue size of a link if initialized
        :return: value to the packet queue size of a link or None if the queue size was not initialized
        """
        return self.max_queue_size


graph = {
    "hosts": [],
    "switches": [],
    "controllers": [],
    "links": []
}

if __name__ == '__main__':

    h1 = Host("h1", "127.0.0.1")
    print(h1)

    s1 = Switch("s1")
    print(s1)

    c1 = Controller("c1")
    print(c1)

    l1 = Link(h1, s1)
    print("l1 first name: " + l1.first.name)

    graph['hosts'].append(h1)
    graph['switches'].append(s1)
    graph['controllers'].append(c1)
    graph['links'].append(l1)

    print(graph)  # uses __repr__ for printing
    print(graph.get('hosts')[0])  # uses __str__ for printing
