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
        return self.first + self.second + " = net.addLink( '" + self.first + "', " + "'" + self.second + "' )\n"

    def to_tuple(self):
        """
        Converts the first and second item into a tuple
        :return: a tuple containing the first and second item
        """
        return tuple((self.first, self.second))


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
