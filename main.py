import random as rd
import numpy as np
import networkx as nx
from networkx import generators as nxgen
import matplotlib.pyplot as plt
import json
import copy
from nltk.corpus import cmudict, wordnet

# a ideia é meio que nas poções, nas armas e nos orbs estão as coisas necessárias
# pra poder construir tudo isso, assim que você achar a sala de craft.

#nltk.download('cmudict')
#nltk.download('punkt')
#nltk.download('wordnet')

# wordnet doc: https://wordnet.princeton.edu/documentation/wngloss7wn
# Synset: A set of synonyms that share a common meaning.
# Hypernym: A more general term that encompasses a broader category in which a specific word belongs. (ex: hyper of dog: animal, mammal, canine)
# Hyponym: A more specific term that fall under the category of a broader term (hypernym) (ex: hypo of dog: golden retriver, poodle, pincher)


class Dungeon():

    def __init__(self,productions_address: str) -> None:
        self.productions = self.get_productions(archive_name=productions_address)
        self.map = self.generate_map(interval=[10,15])
        self.map = self.rooms_connections(map=self.map) 
        self.dungeon = self.build_dungeon(dungeon=self.map)
        self.map_description(map=self.dungeon)
        self.draw_graph(self.dungeon)

    def get_productions(self, archive_name):
        with open (archive_name) as file:
            productions = json.load(file)
        return productions
    
    def get_edge_labels(self, graph:object):
        legend = {}
        target = ["CONNECTION","TRIGGER"]
        free = ["DOOR","PORTAL"]
        lock = ["WEAK_WALL","KEY_DOOR","ORB_PORTAL","STATUE_PORTAL"]
        for edge, atb in graph.edges.items():
            #Gets just the first 3 letter of the production
            for element in target:
                if element in atb:
                    if atb[element] in free: legend[edge] = "FREE"
                    elif atb[element] in lock: legend[edge] = f"{atb[element][0]}_LOCK"
                    else:
                        legend[edge] = f" - {atb[element][0:4]} - "
        return legend
    
    def get_node_color_map(self, graph: object):
        room_nodes = []
        for node in graph.nodes():
            if graph.nodes[node]["TYPE"] == "ROOM":
                room_nodes.append("brown")
            elif graph.nodes[node]["TYPE"] == "ENCOUNTER":
                room_nodes.append("orange")
            elif graph.nodes[node]["TYPE"] == "EXIT":
                room_nodes.append("green")
            else: room_nodes.append("blue")
        return room_nodes
    
    def draw_graph(self, graph: object):
        pos = nx.kamada_kawai_layout(graph)
        nx.draw(G=graph, pos=pos, with_labels=True, node_color=self.get_node_color_map(graph))
        nx.draw_networkx_edge_labels(G=graph, pos=pos, edge_labels=self.get_edge_labels(graph))
        plt.show()

    def map_description(self, map: object):
        output = ""
        output = (f"BEHOLD! The wizzard tower!\n")
        for room in map.nodes():
            if map.nodes[room]["TYPE"]=="ROOM":
                output += (f"   In room {room},\n")
                for connection in nx.neighbors(map,room):
                    if map.nodes[connection]["TYPE"]=="ROOM":
                        index = self.productions["CONNECTIONS"].index(map.edges[room,connection]["CONNECTION"])
                        output += (f"     {self.productions['CONNECTIONS_DESC'][index]}\n")
        print(output)

    def generate_map (self, interval=[5,7]):
        """Returns a graph that represents the tower map.
        if interval has only 1 element, a graph of the element+2 nodes
        if interval has 2 elements, a random graph of the interval+2 nodes"""
        if len(interval)==1: graph_size = interval[0]
        elif len(interval)==2: graph_size = rd.randint(interval[0]-2,interval[1]-2)
        else: raise ValueError("interval must have 1 or 2 elements.")
        prufer_seq = []
        for _ in range(graph_size):
            prufer_seq.append(rd.randint(0,graph_size))
        return (nx.from_prufer_sequence(prufer_seq))    

    def rooms_connections (self, map: object):
        """Returns the graph with labeled edges between the rooms.
        They specify how they are connected."""
        for edge in map.edges():
            map.edges[edge]["CONNECTION"] = self.get_symbol(nonterminal="CONNECTIONS")
            index = self.productions["CONNECTIONS"].index(map.edges[edge]["CONNECTION"])
            #map.edges[edge]["color"] = self.productions["CONNECTIONS_c"][index]
            self.adjust_prob(symbol="CONNECTIONS", index=index)
        return map
    
    def type_encounter_trigger(self, graph, current_node, new_node):
        for node in nx.all_neighbors(graph=graph,node=current_node):
            if isinstance(node,int):
                graph.edges[node,current_node]["TRIGGER"] = self.get_encounter_triggers(production=new_node)
        return graph
        
    def get_encounter_triggers (self, production:str):
        if production in self.productions["auto_trigger"]:
            return "auto"
        elif production in self.productions["interact_trigger"]:
            return "interact"
         
    def build_dungeon(self, dungeon: object):
        room_seq = []
        for node in dungeon: 
            dungeon.nodes[node]["TYPE"] = "ROOM"
            room_seq.append(node)
        for node in reversed(room_seq):
            dungeon = self.build_dungeon_recursive(graph=dungeon, current_node=node)
        return dungeon

    def build_dungeon_recursive(self, graph, current_node, depth=0, max_depth=150): 
        grammar_rule = graph.nodes[current_node]["TYPE"]
        new_node = self.get_symbol(nonterminal=grammar_rule)
    
        #print(f"b4: {self.productions[f'{grammar_rule}_p']}")
        prod_index = self.productions[grammar_rule].index(new_node)
        self.adjust_prob(symbol=grammar_rule, index=prod_index)
        #print(f"after: {self.productions[f'{grammar_rule}_p']}\n")

        self.productions[f"{grammar_rule}_n"][prod_index] += 1
        qty = self.productions[f"{grammar_rule}_n"][prod_index]
        new_node_id = (f"{new_node}_{qty}")

        graph.add_node(new_node_id)
        graph.nodes[new_node_id]["TYPE"] = new_node
        graph.add_edge(current_node, new_node_id)
        if grammar_rule == "ENCOUNTER":
            graph = self.type_encounter_trigger(graph, current_node, new_node)
        if graph.nodes[new_node_id]["TYPE"] in self.productions:
            self.build_dungeon_recursive(graph, new_node_id, depth+1, max_depth)
        return graph          

    def adjust_prob(self, symbol:str, index:int):
        """rule: which production will be adjusted,
        index: which index of production"""
        old_prob = copy.deepcopy(self.productions[f"{symbol}_p"])
        new_prob = self.productions[f"{symbol}_p"]
        multiplier = self.productions[f"{symbol}_d"][index]
        new_prob[index] *= (1-multiplier)
        if multiplier==0: adjustment=0
        else: adjustment = (old_prob[index] - new_prob[index])/(len(new_prob)-1)
        for i,each in enumerate(new_prob):
            if i!=index: 
                new_prob[i] += adjustment        

    def get_symbol(self,nonterminal:str):
        symbol = rd.choices(self.productions[nonterminal], weights=self.productions[f"{nonterminal}_p"])
        return symbol[0]

def demo():
    myDg = Dungeon("productions.json")
    print("============")
    #print(myDg.map)
    #myDg.draw_tower_map()

if __name__ == "__main__":
    demo()


"""
You are free.
You not sure how long you have been locked into that magical prison, but you're free now. 
The bad part is that you are still inside the wizard's tower. The same one you and your band were invading to fulfill a contract. Are you friends even alive? 
The good part is that the tower's automatic defenses don't seem to recognize you as a threat. Yet.
In the room your are in, you see a scroll with a map... 



dungeon -> list of rooms, with entrance, middle and final.

usable -> potions, magical scrolls
carryable -> weapons, armors, key_items
lore -> scrolls to read, books to read, annotations
enemy -> enemies(animals, zombies, skeletons, shadows)


In this dungeon there are [number] of rooms.

DUNGEON -> Room
ROOM -> <ENCOUNTER> | <ROOM> | ε
ENCOUNTER -> <LORE> | <USABLE> | <CARRYBLE> | <ENEMY> | <ENCOUNTER> | ε
LORE -> 
USABLE -> <+hp> | <-hp> | <invisible> | <super_strenght> | <blind> | <death> | ε
CARRYABLE -> <WEAPON> | <KEY_ITEM>
WEAPON -> sword | crossbow with 1 arrow | staff
KEY_ITEM -> orb | book | key
"""