from rules import Rule
from graph_grammar import GraphGrammar
import matplotlib.pyplot as plt
import networkx as nx
import json
import random as rd
import re

class WizarDDungeon():
    def __init__(self, grammar_file: str) -> None:
        self.grammar = GraphGrammar(file_name=grammar_file)
        self.dungeon_iterations = [self.create_dungeon()]     
        
    def create_dungeon(self):
        graph = nx.DiGraph()
        graph.add_node("EN:1", type="room")
        return graph
    
    def creation_loop(self):
        #apply first rule to initial node
        dungeon = self.grammar.apply_rule(target_hook="EN:1",
                                graph=self.dungeon_iterations[0],
                                rule=self.grammar.rules[0])
        self.dungeon_iterations.append(dungeon)
        
        #apply rule 1 random number of times for all nodes in graph:
            #TODO:LOOP [X TIMES]THROUGH ALL GRAPH NODES AND APPLY RULE 1 ONCE ON ALL POSSIBLE NODES.
        
        
        self.grammar.draw_graph([[
            "DUNGEON",dungeon
        ]])
        
        
        
        
        return self.dungeon
        

if __name__ == "__main__":
    dungeon = WizarDDungeon(grammar_file="graph_productions.json")
    dungeon.creation_loop()
    