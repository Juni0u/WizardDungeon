from rules import Rule
import matplotlib.pyplot as plt
import networkx as nx
import json
import random as rd
import re
import os


class GraphGrammar():
    
    def __init__(self,file_name:str) -> None:
        self.file_name = file_name
        self.rules = []
        self.left_side = []
        self.right_side = [] 
        self.read_rules()
        
    def draw_graph(self, graphs: list[list[str,nx.DiGraph]]):
        """_summary_

        Args:
            graphs (list[list[str,nx.DiGraph]]): _[[figurename,graph]]_
        """
        for _, graph in enumerate(graphs):
            #pos = nx.kamada_kawai_layout(graph[1])
            plt.figure(graph[0])
            pos = nx.planar_layout(graph[1])
            nx.draw_networkx_nodes(G=graph[1],pos=pos,
                    linewidths= 2,
                    edgecolors= "black",
                    node_color=[graph[1].nodes[node]["color"] for node in graph[1].nodes], 
                    node_size=500)
            nx.draw_networkx_edges(G=graph[1],pos=pos, width=1.5,
                                   edge_color=[graph[1].edges[edge]["color"] for edge in graph[1].edges])
            nx.draw_networkx_labels(G=graph[1],pos=pos,font_size=8)
            
        plt.show()        
        
    def draw_rules(self):
        for i,rule in enumerate(self.rules):
            fig, axs = plt.subplots(1,len(rule.right_side)+1, figsize=(10,10))
            axs[0] = nx.draw(G=rule.left_side, with_labels=True, node_color="#828282", node_size=500, ax=axs[0])
            for j,rs in enumerate(rule.right_side):
                axs[j+1] = nx.draw(G=rs, with_labels=True, 
                                   node_color="#828282", 
                                   node_size=500, ax=axs[j+1])
            fig.tight_layout()
            path = os.path.join("imgs", f"rule{i}.png")
            plt.savefig(path)
    
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
    
    def apply_rule(self, target_hook: str, graph:nx.DiGraph, rule:Rule):
        """
        target_hook = hook node in graph to be transformed
        graph = target graph
        rule = target rule
        Given a graph and a rule, apply the rule to a node/group of nodes
        """
        if not rule.rule_correspondence(graph): 
            return graph #No rule correspondence, returns the same graph
        
        #save hook's current edges
        hook_edges = []
        for source, target, atributes in graph.edges(data=True):
            if (source==target_hook) or (target==target_hook):
                hook_edges.append((source,target,atributes))
                
        #Get production from right_side of the rule
        production = rule.right_side[rd.randint(0,len(rule.right_side)-1)] # select a random production from the right side of the rule #TODO: Use probabilities later
        
        #Count number how many times each node from right_side appears in the graph
        #And maps the modifications of labels
        node_counter = {}
        rename_dict = {}
        for rule_node in production.nodes():
            rule_node_type = re.split(":",rule_node)[0]                

            #build dict with new labels
            if production.nodes[rule_node]["isHook"]:
                rename_dict[rule_node] = target_hook
            else:
                rename_dict[rule_node] = (f"{rule_node_type}:")    
            
            #count and fill counter dict
            if rule_node_type not in node_counter:
                node_counter[rule_node_type] = 0
            else: 
                continue
            for graph_node in graph.nodes():
                graph_node_type = re.split(":",graph_node)[0]
                if rule_node_type == graph_node_type:
                    node_counter[rule_node_type] += 1   
        
        # finish mapping node labels and changing labels
        for i, node in enumerate(rename_dict):
            if production.nodes[node]["isHook"]:
                continue
            node_type = re.split(":",node)[0]
            if node_type in rename_dict[node]:
                rename_dict[node] += (f"{node_counter[node_type]+i}")
        
        production = nx.relabel_nodes(production, rename_dict)
        
        #removing hook from graph
        mod_graph = graph.copy()        
        mod_graph.remove_node(target_hook)
        
        #add production to graph
        for node, atributes in production.nodes(data=True):
            mod_graph.add_node(node, **atributes)
            
        for source, target, atributes in production.edges(data=True):
            mod_graph.add_edge(source, target, **atributes)
        
        #add edges that were linked to hook of old graph
        if len(hook_edges) > 0:
            for edge in hook_edges:
                mod_graph.add_edge(edge[0], edge[1], **edge[2])
                
        return mod_graph        

def exemple_graph(opt,node_number=0):
    if opt=="i": #initial room
        G = nx.DiGraph()
        G.add_node("EN:1", type="room")
        return G
    
    if opt=="t": #test graph
        G = nx.DiGraph()
        G.add_node("EN:1", type="room")
        G.add_node("R:1", type="room")
        G.add_node("R:2", type="room")
        G.add_node("R:3", type="room")
        G.add_edge("EN:1","R:1", type="connection", status="free")
        G.add_edge("EN:1","R:2", type="connection", status="free")
        G.add_edge("EN:1","R:3", type="connection", status="free")
        return G
    else: 
        G = nx.DiGraph()
        max_n = rd.randint(5,10)
        for i in range(max_n):
            G.add_node(i)
        return G
    

def demo():
    grammar = GraphGrammar(file_name="graph_productions.json")
    graph = exemple_graph(opt="t")
    graph2 = grammar.apply_rule("R:1",graph,grammar.rules[1])
    #grammar.draw_graph([["teste",graph],["regra1",graph2]])
    
    for edge in graph2.edges():
        print(edge)
        print(graph2.edges[edge])
    
    print("==========OUTPUT==========")

if __name__ == "__main__":
    demo()
