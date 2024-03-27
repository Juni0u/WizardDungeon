import matplotlib.pyplot as plt
import networkx as nx
import re

class Rule():
    def __init__(self, left_side, right_side) -> None:
        self.left_side = left_side
        self.right_side = right_side

    def add_name(self, name):
        """Puts a name in the rule"""
        self.name = name
    
    def get_left_nodes(self):
        """Returns an iterator of all nodes in the left side of the rule without numbers"""
        nodes = nx.nodes(self.left_side)
        return nodes
    
    def get_right_nodes(self):
        """Returns a list of iterators of all nodes without numbers for each graph in the right side of the rule """
        nodes = []
        for production in self.right_side:
            nodes.append(nx.nodes(production))
        return nodes
    
    def get_left_edges(self):
        """Returns the edges without numbers of the left side of the rule"""
        return list(nx.edges(self.left_side))

    def get_right_edges(self):
        """Returns a list of the edges without numbers of each graph in the right side of the rule"""
        edges = []
        for production in self.right_side:
            edges.append(list(nx.edges(production)))
        return edges
    
    def node_correspondence(self, graph):
        """Returns TRUE if all nodes from left side are present in [graph]"""
        graph_nodes = [(re.split(":",graph_node)[0]) for graph_node in graph.nodes()]
        for rule_node in self.get_left_nodes():         
            if rule_node not in graph_nodes:
                return False
        return True
    
    def edge_correspondence(self, graph):
        """Returns TRUE if all edges from left side are present in [graph]"""
        rule_edges = self.get_left_edges()
        if len(rule_edges)==0: 
            return True #there are no edges in rule, so just node is needed.
        graph_edges = [(re.split(":",source)[0], re.split(":",target)[0]) for source, target in graph.edges()]
        for rule_edge in rule_edges:
            if rule_edge not in graph_edges:
                return False
        return True        
    
    def rule_correspondence(self, graph):
        if (self.node_correspondence(graph)) and (self.edge_correspondence(graph)):
            return True
        else: return False
        

    