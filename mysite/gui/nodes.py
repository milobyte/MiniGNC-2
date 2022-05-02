"""
This file contains classes for nodes in the network
__author__: Gatlin Cruz
__author__: Cade Tipton
__author__: Noah Lowry
__author__: Miles Stanley
__version__: 12/2/21
"""


class Host:
    """
    This class represents a Host object within the network.
    author: Originally written by Cade Tipton and Gatlin Criz
    author: Additional modifications by Miles Stanley (80%)
    """
    def __init__(self, name, ip):
        """
        Creates a new Host object
        :param name: The name of the host
        :param ip: The ip of the host
        :return: None
        """
        self.name = name
        self.type = 'host'
        self.ip = ip
        self.link_log = ['No IPERF data', 'No PING data']
        self.IPERF_LOG = 0
        self.PING_LOG = 1


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

    def get_type(self):
        """
        Getter for the type of node this is
        :return: type The type of node this object represents
        """
        return self.type

    def set_link_log(self, type, output):
        """
        Sets either the latest iPerf or Ping test information
        :param type: the type of test (iPerf or Ping) whose information should be updated
        :param output: the information that represents the result of the latest test
        :return: None
        """
        if type == 'iperf':
            # print("New iperf for " + self.name + " recorded")
            self.link_log[self.IPERF_LOG] = output
        elif type == 'ping':
            # print("New ping for " + self.name + " recorded")
            self.link_log[self.PING_LOG] = output

    def get_iperf_log(self):
        """
        Returns the latest Ping information
        :return: the latest Ping information
        """
        return self.link_log[self.IPERF_LOG].replace("'", "")

    def get_ping_log(self):
        """
        Returns the latest iPerf information
        :return: the latest iPerf information
        """
        return self.link_log[self.PING_LOG].replace("'", "")

    def equals(self, other):
        """
        Returns True is the object is equal, False otherwise
        :param other: the comparing object
        """
        if(type(other) == Host):
            if((self.name == other.get_name() and self.ip == other.get_ip())):
                return True
        return False


class Switch:
    """
    This class represents a Switch object within the network.
    author: Originally written by Cade Tipton and Gatlin Criz
    author: Additional modifications by Miles Stanley (40%)
    """
    def __init__(self, name):
        """
        Creates a new Switch object
        :param name: The name of the switch
        :return: None
        """
        self.name = name
        self.type = 'switch'

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

    def get_type(self):
        """
        Getter for the type of node this is
        :return: type The type of node this object represents
        """
        return self.type

    def equals(self, other):
        """
        Returns True is the object is equal, False otherwise
        :param other: the comparing object
        """
        if(type(other) == Switch):
            if((self.name == other.get_name())):
                return True
        return False


class Controller:
    """
    This class represents a Controller object within the network.
    author: Originally written by Cade Tipton and Gatlin Cruz
    """
    def __init__(self, name):
        """
        Creates a Controller object
        :param name: The name of the controller
        :return: None
        """
        self.name = name
        self.type = 'controller'

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

    def get_type(self):
        """
        Getter for the type of node this is
        :return: type The type of node this object represents
        """
        return self.type

    def equals(self, other):
        """
        Returns True is the object is equal, False otherwise
        :param other: the comparing object
        """
        if(type(other) == Controller):
            if((self.name == other.get_name())):
                return True
        return False


class Link:
    """
    This class represents a Host object within the network.
    author: Originally written by Cade Tipton and Gatlin Criz
    author: Additional modifications by Noah Lowry and Miles Stanley (90%)
    """
    def __init__(self, first, second):
        """
        Creates a Link object
        :param first: The first item in the link
        :param second: The second item in the link
        :return: None
        """
        self.first = first
        self.second = second
        self.type = 'type'
        self.bandwidth = 10 
        self.delay = '0ms'
        self.loss = '0'
        self.max_queue_size = '1000'

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

        # Defining the linkOpts object for defining link parameters
        linkOptsString = ("link_opts = dict(bw = " + str(self.bandwidth) + ", delay = '" + str(self.delay) + 
            "', loss = " + str(self.loss) + ", max_queue_size = " + str(self.max_queue_size) + ")\n")
        
        # Defining the addLink function with linkOpts
        linkInitializer = (linkOptsString + self.first + self.second + " = net.addLink( '" + 
            self.first + "', " + "'" + self.second + "', **link_opts )\n")
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

    def get_first(self):
        """
        Returns the name of the first host
        :return: the name of the first host
        """
        return self.first

    def get_second(self):
        """
        Returns the name of the second host
        :return: the name of the second host
        """
        return self.second

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

    def get_loss(self):
        """
        Returns the value representing the precentage of loss in packets of a link 
        :return: representing the precentage of loss in packets of a link  or None if loss was not initialized
        """
        return self.loss

    def set_loss(self, loss):
        """
        Sets a value representing the precentage of loss in packets of a link 
        :param loss: the precentage of loss in packets of a link 
        :return: None
        """
        # SET RESTRICTIONS
        self.loss = loss
        print("LOSS: " + loss + " ADDED")

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

    def get_type(self):
        """
        Getter for the type of node this is
        :return: type The type of node this object represents
        """
        return self.type

    def equals(self, other):
        """
        Returns True is the object is equal, False otherwise
        :param other: the comparing object
        """
        if(type(other) == Link):
            if((self.first == other.get_first() and self.second == other.get_second())):
                return True
        return False


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
