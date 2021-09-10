from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
from pathlib import Path


class App:

    def __init__(self, uri, username, pw):
        """
        The constructor for the App object
        :param uri: The uri that is being used
        :param username: The username that is used to gain access to the database
        :param pw: The password that is used to gain access to the database
        """
        self.driver = GraphDatabase.driver(uri, auth=(username, pw))

    def close(self):
        """
        Cooses the driver object connection
        :return: None
        """
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()

    @staticmethod
    def _create_and_return_node(tx, node, graph_name, node_type, ip=None):
        """
        Creates a node to the database
        :param tx: The tx object used to run the command
        :param node: The node object that's being added
        :return: The result from the function call
        """
        if ip is None:
            query = ("CREATE (p1:" + str(graph_name) + "{ name: $node, type: '" + str(node_type) + "' }) RETURN p1")
        else:
            query = ("CREATE (p1:" + str(graph_name) + "{ name: $node, type: '" +
                     str(node_type) + "' , ip: '" + str(ip) + "' }) RETURN p1")

        return tx.run(query, node=node, graph_name=graph_name).single()

    def create_node(self, node_name, graph_name, node_type, ip=None):
        """
        Calls the static method _create_and_return to add a single node
        :param ip: The IP of the node if it is specified, or None otherwise
        :param node_type: The type of the node (host, switch, or controller)
        :param graph_name: the name of the graph
        :param node_name: The name of the node
        :return: The result from the function call
        """
        with self.driver.session() as session:
            return session.write_transaction(self._create_and_return_node, node_name, graph_name, node_type, ip)

    @staticmethod
    def _create_and_return_links_db(tx, node1, node2, graph_name):
        """
        Creates the links between the nodes
        :param tx: the object that runs the query
        :param node1: the starting node in the link
        :param node2: the ending node in the link
        :return: the result of the function call
        """

        return tx.run("MATCH (a:{}), (b:{}) WHERE a.name = '{}' AND b.name = '{}'CREATE (a)-[r:PORT]->(b)RETURN "
                      "type(r)".format(graph_name, graph_name, node1, node2))

    def create_links_db(self, node1, node2, graph_name):
        """
        Calls _create_and_return_links_db method
        :param graph_name: the name of the graph
        :param node1: the starting node in the link
        :param node2: the ending node in the link
        :return: the result of the function call
        """
        with self.driver.session() as session:
            return session.write_transaction(self._create_and_return_links_db, node1, node2, graph_name)

    def create_csv(self, filename):
        """
        Calls the static method _create_csv to export the csv file
        :param filename: The name of the file
        :return: The result from the function call
        """
        with self.driver.session() as session:
            return session.write_transaction(self._create_and_return_csv, filename)

    @staticmethod
    def _create_and_return_csv(tx, filename):
        """
        Creates the links between the nodes
        :param tx: the object that runs the query
        :param filename: the name of the file
        :return: the result of the function call
        """

        path = str(Path.home()) + "/Desktop/" + str(filename) + ".csv"
        return tx.run("CALL apoc.export.csv.all($path, {})", path=path).single()

""" Used to test """
if __name__ == "__main__":
    # Aura queries use an encrypted connection using the "neo4j+s" URI scheme
    bolt_url = "neo4j://localhost:7687"  # %%BOLT_URL_PLACEHOLDER%%
    user = "neo4j"
    password = "mininet"
    app = App(bolt_url, user, password)
    app.create_friendship("Alice", "David")
    app.find_person("Alice")
    app.close()
