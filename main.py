import random as rd
import numpy as np
import networkx as nx
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
        #self.test_probs()
        self.build_dungeon()

    def get_productions(self, archive_name):
        with open (archive_name) as file:
            productions = json.load(file)
        return productions
    
    def draw_graph(self, graph: object):
        nx.draw(graph, with_labels=True)
        plt.show()
        self.check_rooms_filled(graph=graph)
    def check_rooms_filled(self, graph):
        for node in graph.nodes():
            if "ROOM" in node:
                neighbors = list(graph.neighbors(node))
                #print(node, neighbors)
                if "ENCOUNTER" not in neighbors:
                        return False, node
        return True, 0
    #TODO: Nao estou entendendo pq algumas ROOMS tem mais de um ENCOUNTER.
    #TODO: Tambem nao estou entendendo como as recursoes estao parando - o caso base nao esta bom o suficiente
    #eu acho que na funcao check rooms fillet ela nao ta vendo as salas direito, ou ta pegando sempre so a primeira sala.
    #TODO: Tendo umas divisoes por zero tambem
    #TODO: Ideia é refazer essa parte toda
    def build_dungeon(self, depth=0, max_depth=11):
        dgg = nx.DiGraph()
        dgg.add_node("ROOM")
        dgg = self._build_dungeon_recursive(dgg, "ROOM")
        self.draw_graph(dgg)

    def _build_dungeon_recursive(self, graph, current_node, depth=0, max_depth=150): 
        if depth >= max_depth: return graph
        # Get next production

        check_node = current_node.split("_")[0]
        # max_num_branches = 3 if check_node == "ROOM" else 1
        max_num_branches = 1

        has_encounter = False

        for _ in range(max_num_branches):
            if has_encounter:
                break

            new_node = self.get_symbol(nonterminal=check_node)

            if new_node == "ENCOUNTER":
                has_encounter = True
        
            if new_node in graph.nodes():
                print(self.productions["ROOM_p"])
                index = self.productions[check_node].index(new_node)
                self.adjust_prob(symbol=check_node, index=index)
                new_node_id = f"{new_node}_{len(graph.nodes())}"
                print(self.productions["ROOM_p"])
            else:
                new_node_id = new_node

            # create a new node and recurse if not a terminal
            
            graph.add_node(new_node_id)
            graph.add_edge(current_node, new_node_id)
            if new_node_id.split("_")[0] in self.productions:
                self._build_dungeon_recursive(graph, new_node_id, depth+1, max_depth)
        return graph          

    def adjust_prob(self, symbol:str, index:int):
        """rule: which production will be adjusted,
        index: which index of production"""
        old_prob = copy.deepcopy(self.productions[f"{symbol}_p"])
        new_prob = self.productions[f"{symbol}_p"]
        new_prob[index] *= (1-self.productions[f"{symbol}_d"][index])
        adjustment = (old_prob[index] - new_prob[index])/(len(new_prob)-1)
        for i,each in enumerate(new_prob):
            if i!=index: 
                new_prob[i] += adjustment        

    def get_symbol(self,nonterminal:str):
        symbol = rd.choices(self.productions[nonterminal], weights=self.productions[f"{nonterminal}_p"])
        return symbol[0]

def demo():
    myDg = Dungeon("/home/nonato/GitRepository/Grammar Studies/Dungeon/productions.json")
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