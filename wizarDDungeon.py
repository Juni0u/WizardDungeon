from rules import Rule
from graph_grammar import GraphGrammar
import matplotlib.pyplot as plt
import networkx as nx
import random as rd
import os
from datetime import datetime


class WizarDDungeon():
    def __init__(self, grammar_file: str, base_adress: str) -> None:
        self.grammar = GraphGrammar(file_name=grammar_file)
        self.dungeon_folder = self.create_dungeon_folder(adress=base_adress)
        self.dungeon = self.create_dungeon()  
        
    def create_dungeon_folder(self, adress):
        time = datetime.now().strftime("%Y%m%d-%H%M%S")       
        folder_path = adress + f"TOWER_{time}"
        os.makedirs(folder_path)
        return folder_path
        
    def save_dg_fig(self, fig_name:int, graph:nx.DiGraph) -> None:        
        pos = nx.planar_layout(graph)
        plt.figure()
        nx.draw(G=graph, pos=pos, with_labels=True, node_color="red", node_size=500)
        file_path = os.path.join(self.dungeon_folder, f"{fig_name}.png")
        plt.savefig(file_path) 
        
    def create_dungeon(self) -> nx.DiGraph:
        graph = nx.DiGraph()
        graph.add_node("EN:1", type="initial_room")
        self.save_dg_fig(fig_name="initial_dungeon",graph=graph)
        return graph
    
    def creation_loop(self) -> nx.DiGraph:
        #apply first rule to initial node
        start_dungeon = self.grammar.apply_rule(target_hook="EN:1",graph=self.dungeon,rule=self.grammar.rules[0])
        self.save_dg_fig(fig_name="iter 1",graph=start_dungeon)
                
        #dungeon rooms loop
        #---apply rule 1 a number of times for all nodes in graph:
        times = self.dice_roller(rolls=2, sides=2)
        self.dungeon = self.dungeon_rooms_loop(iterations=times, dungeon=start_dungeon)
        self.save_dg_fig(fig_name="final_dungeon",graph=self.dungeon)
        return self.dungeon
    
    def dice_roller(self, rolls:int, sides:int):
        value = 0        
        for _ in range(rolls):
            value += rd.randint(1,sides)
        return value
    
    def dungeon_rooms_loop(self, iterations:int, dungeon:nx.DiGraph, max_iterations=10) -> nx.DiGraph:
        """Returns the dungeon in the end of the loop."""
        iteration = 2
        last_rooms = []
        for i in range(iterations):
            target_nodes = self.seek_nodes(graph=dungeon, node_type="R")                 
            for node in target_nodes:
                if node in last_rooms: #if node was modified last iteration, it wont be in this one
                    last_rooms.remove(node)
                    continue
                dungeon = self.grammar.apply_rule(target_hook=node,graph=dungeon,rule=self.grammar.rules[1])
                self.save_dg_fig(fig_name=f"iter {iteration}",graph=dungeon)
                last_rooms.append(node)
                iteration += 1
                if iteration > max_iterations: break
        return dungeon

        
    def seek_nodes(self, graph:nx.DiGraph, node_type:str):
        """Returns a list of all nodes of that type in the graph"""
        nodes = []
        for node in graph.nodes():
            if node_type in node:
                nodes.append(node)
        return nodes
        
        
        

if __name__ == "__main__":
    dungeon = WizarDDungeon(grammar_file="graph_productions.json",
                            base_adress="/home/nonato/GitRepository/WizardDungeon/TowerUniverse/")
    dungeon.creation_loop()
    