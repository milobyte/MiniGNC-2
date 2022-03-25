from neo4j import GraphDatabase
import logging
from neo4j.exceptions import ServiceUnavailable
from pathlib import Path


class App:
    def __init__(self, uri, username, pw, graph_name = None):
        """
        The constructor for the App object
        :param uri: The uri that is being used
        :param username: The username that is used to gain access to the database
        :param pw: The password that is used to gain access to the database
        """
  
        self.driver = GraphDatabase.driver(uri, auth=(username, pw))
        if graph_name is not None:
            with self.driver.session() as session:
                print("Creating New Database")
                print(session.write_transaction(self._create_database, graph_name))

    def close(self):
        """
        Closes the driver object connection
        :return: None
        """
        # Don't forget to close the driver connection when you are finished with it
        self.driver.close()
    
    @staticmethod
    def _create_database(tx, graph_name):
        query = "CREATE or REPLACE DATABASE " + graph_name
        return tx.run(query)

    @staticmethod
    def _use_database(tx, graph_name):
        query = "use " + graph_name
        return tx.run(query)

    @staticmethod
    def _create_and_return_node(tx, node, graph_name, node_type, ip=None, iperf_log=None, ping_log=None):
        """
        Creates a node to the database
        :param tx: The tx object used to run the command
        :param node: The node object that's being added
        :param node_type: The type of the node (host, switch, or controller)
        :param graph_name: the name of the graph
        :return: The result from the function call
        """

        # REDO WITH STRING FORMATTING
        # LOGGING SYNTAX ERROR
        if ip is None:
            query = ("CREATE (p1:" + str(graph_name) + "{ name: $node, type: '" + str(node_type) + "' }) RETURN p1")
        else:
            query = ("CREATE (p1:" + str(graph_name) + "{ name: $node, type: '" +
                     str(node_type) + "' , ip: '" + str(ip) + "', iPerf_data: '" + str(iperf_log) + "', ping_data: '" + str(ping_log) + "' }) RETURN p1")

        return tx.run(query, node=node, graph_name=graph_name).single()

    def create_node(self, node_name, graph_name, node_type, ip=None, iperf_log=None, ping_log=None):
        """
        Calls the static method _create_and_return to add a single node
        :param ip: The IP of the node if it is specified, or None otherwise
        :param node_type: The type of the node (host, switch, or controller)
        :param graph_name: the name of the graph
        :param node_name: The name of the node
        :return: The result from the function call
        """
        # iperf_log = "'" + iperf_log + "'"
        # print(ping_log)
        with self.driver.session(database=graph_name) as session:
            return session.write_transaction(self._create_and_return_node, node_name, graph_name, node_type, ip, iperf_log, ping_log)

    @staticmethod
    def _create_and_return_links_db(tx, node1, node2, graph_name, bw, delay, loss, queue_size):
        """
        Creates the links between the nodes
        :param tx: the object that runs the query
        :param node1: the starting node in the link
        :param node2: the ending node in the link
        :return: the result of the function call
        """
        query = ("MATCH (a:{}), (b:{})"
                "WHERE a.name = '{}' AND b.name = '{}'"
                "CREATE (a)-[r:PORT {{bandwidth: '{}', delay: '{}', loss: '{}', queue_size: '{}'}}]->(b) "
                "return type(r)".format(graph_name, graph_name, node1, node2, bw or "unlimited", delay or "none", loss or "none", queue_size or "none"))
        return tx.run(query)

    def create_links_db(self, node1, node2, graph_name, bw, delay, loss, queue_size):
        """
        Calls _create_and_return_links_db method
        :param graph_name: the name of the graph
        :param node1: the starting node in the link
        :param node2: the ending node in the link
        :return: the result of the function call
        """
        # print(node1 + " " + node2)
        with self.driver.session(database=graph_name) as session:
            return session.write_transaction(self._create_and_return_links_db, node1, node2, graph_name, bw, delay, loss, queue_size)

    def create_csv(self, filename):
        """
        Calls the static method _create_csv to export the csv file
        :param filename: The name of the file and graph database
        :return: The result from the function call
        """
        with self.driver.session(database=filename) as session:
            return session.write_transaction(self._create_and_return_csv, filename)

    @staticmethod
    def _create_and_return_csv(tx, filename):
        """
        Exports the database as a CSV file to the Desktop directory
        :param tx: the object that runs the query
        :param filename: the name of the file
        :return: the result of the function call
        """
        # PATH USED FOR STANDARD NEO4J INSTALLATION
        # path = str(Path.home()) + "/Desktop/" + str(filename) + ".csv"

        # NEW PATH BASED ON NEO4J DESKTOP (CSV FILES ARE IN THE IMPORT DIRECTORY)
        path = str(filename) + ".csv"
        return tx.run("CALL apoc.export.csv.all($path, {})", path=path).single()

    def run_single_data_query(self, db, spec):
        """
        Calls the static method that runs a condtional query in the database
        :param spec: The conditional string used to run the query
        :return: The result from the function call
        """
        with self.driver.session(database=db) as session:
            return session.write_transaction(self._run_single_query, spec)
            


    @staticmethod 
    def _run_single_query(tx, spec):
        """
        the static method that runs a condtional query in the database
        :param spec: The conditional string used to run the query
        :return: The result from the function call
        """
        print("MATCH (s:example)-[r:PORT]->(d:example) WHERE " + spec + " RETURN s.name,d.name")
        query1 = ("MATCH (s:example)-[r:PORT]->(d:example) WHERE " + spec + " RETURN s.name,d.name")
        results = tx.run(query1)

        for record in enumerate(results):
            print(record[1].value(0) + " -> " + record[1].value(1))

        return results

    # ADDED FUNCTIONS 1/22/2022
    def clear_data(self, db):
        """
        Calls the static method _clear_database to delete all nodes and relationships in the database
        :return: The result from the function call
        """
        with self.driver.session(database=db) as session:
            return session.write_transaction(self._clear_database)

    @staticmethod
    def _clear_database(tx):
        """
        Clears the database of all nodes and relationships.
        :param tx: the object that runs the query
        :return: the result of the function call
        """
        query1 = ("MATCH (n)"
                 "DETACH DELETE n")
        return tx.run(query1).single()

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
