from rules import Rule
import matplotlib.pyplot as plt
import networkx as nx
import json
import random as rd

class GraphGrammar():
    
    def __init__(self,file_name:str) -> None:
        self.file_name = file_name
        self.rules = []
        self.left_side = []
        self.right_side = [] 
        self.read_rules()
        
    def draw_graph(self, graph: object):
        pos = nx.kamada_kawai_layout(graph)
        nx.draw(G=graph, pos=pos, with_labels=True, node_color="red", node_size=500)
        plt.show()        
    
    def create_graph(self, graph_data:dict):
        graph = nx.DiGraph()
        for node in graph_data["nodes"]:
            node_attributes = {}
            for key, value in node.items():
                if key != "id":
                    node_attributes[key] = value                   
            graph.add_node(node["id"], **node_attributes)

        for edge in graph_data["edges"]:
            edge_attributes = {}
            for key, value in edge.items():
                if (key != "source") and (key != "target"):
                    edge_attributes[key] = value  
            graph.add_edge(edge["source"],edge["target"], **edge_attributes)
        return graph
    
    def read_rules(self):
        with open (self.file_name, "r") as json_file:
            data = json.load(json_file)
 
        for rule, rule_data in data.items():
            current_right_side = []
            for data in rule_data: 
                self.left_side.append(self.create_graph(graph_data=data["left_side"]))
                for i,r_data in enumerate(data["right_side"]):
                    current_right_side.append(self.create_graph(graph_data=r_data))
                
                self.rules.append(Rule(left_side=self.create_graph(graph_data=data["left_side"]),
                                    right_side=current_right_side))
                self.right_side.append(current_right_side)
        
        a=0
        if a==1:    
            for index in range(len(self.left_side)):
                print(f"rule{index}")
                print(f"left: {self.left_side[index]}")
                for index2 in range(len(self.right_side[index])):
                    print(f"right{index2}: {self.right_side[index][index2]}")
                print()             
    
    def apply_rule(self, node, graph:nx.DiGraph, rule:Rule):
        """Given a graph and a rule, apply the rule to a node"""
        if not rule.rule_correspondence: 
            return graph #No rule correspondence, returns the same graph
        mod_graph = graph.copy()
        #TODO: Tenho que identificar se a regra ta no grafo e aplicar a transformacao
        
        
        
        return mod_graph
        

def exemple_graph(opt,node_number=0):
    if opt=="i": #first node to start rooms
        G = nx.DiGraph()
        G.add_node("EN", type="room")
        """G.add_node("R:1", type="room")
        G.add_node("R:2", type="room")
        G.add_node("R:3", type="room")
        G.add_edge("EN","R:1", type="connection", status="free")
        G.add_edge("EN","R:2", type="connection", status="free")
        G.add_edge("EN","R:3", type="connection", status="free")"""
        return G
    else: 
        G = nx.DiGraph()
        max_n = rd.randint(5,10)
        for i in range(max_n):
            G.add_node(i)
        return G
    

def demo():
    grammar = GraphGrammar(file_name="graph_productions.json")
    print("============")
    dungeon = exemple_graph(opt="i")
    nodes = grammar.rules[1].edge_correspondence(graph=dungeon)
    print(nodes)
    #grammar.apply_rule(graph=
    # dungeon, rule=grammar.) 



if __name__ == "__main__":
    
    demo()
