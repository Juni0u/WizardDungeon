import matplotlib.pyplot as plt
import networkx as nx
import json

class GraphGrammar():
    
    def __init__(self,file_name:str) -> None:
        """The idea is that to each element in [left_side] theres an element in [right_side]
        It is possible that one element in [left_side] can be mapped to more than more element in [right_side]
        Each element in [right_side] must have an equivalent probability written in [right_probs].
        
        ex >>>
        ----left side-----|--------right side--------|-------right side probs-------|
            [G1,G2]         [[Ga,Gb],[Gc,Gd,Ge]]       [[0.5,0.5],[0.6,0.2,0.2]]
            
        G1 may substituted for Ga or Gb, where each have an 0.5 probability of happening.        
        #TODO: Isso provavelmente sera adaptado pq e melhor ler isso de um arquivo, mas eu tenho que ver como eu leio grafos de um arquivo.
        """
        self.file_name = file_name
        self.left_side = []
        self.right_side = [] 
        
    def draw_graph(self, graph: object):
        pos = nx.kamada_kawai_layout(graph)
        nx.draw(G=graph, pos=pos, with_labels=True)
        plt.show()        
    
    def create_graph(self, graph_data:dict):
        graph = nx.Graph()
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
                self.right_side.append(current_right_side)
        
        a=1
        if a==1:    
            for index in range(len(self.left_side)):
                print(f"rule{index}")
                print(f"left: {self.left_side[index]}")
                for index2 in range(len(self.right_side[index])):
                    print(f"right{index2}: {self.right_side[index][index2]}")
                print()             
    
    def find_subgraph(self):
        pass
        

def demo():
    myGr = GraphGrammar(file_name="graph_productions.json")
    myGr.read_rules()
    print("============")
    



if __name__ == "__main__":
    demo()
