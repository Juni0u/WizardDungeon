from rules import Rule
from graph_grammar import GraphGrammar
import matplotlib.pyplot as plt
import networkx as nx
import random as rd
import os
from datetime import datetime


class WizarDDungeon():
    def __init__(self, grammar_file: str) -> None:
        self.grammar = GraphGrammar(file_name=grammar_file)
        
    def read_layout_from_file(self,graphml_file:str) -> nx.DiGraph:
        return nx.read_graphml(graphml_file)
    
    def fill_color_map(self, graph:nx.DiGraph) -> nx.DiGraph:
        """Adds atribute "color" for each node based on its type.

        Args:
            graph (nx.DiGraph): graph to be transformed

        Returns:
            nx.DiGraph: graph where "color" attribute for each node
        """
        for edge in graph.edges():
            if graph.edges[edge]["status"] == "locked": 
                graph.edges[edge]["color"] = "red"
            else:  
                graph.edges[edge]["color"] = "black" 


        for node in graph.nodes():
            if "EN" in node:
                graph.nodes[node]["color"] = "cyan"
            elif "EX" in node:
                graph.nodes[node]["color"] = "green"
            else:
                graph.nodes[node]["color"] = "white"
        return graph

    def create_dungeon_folder(self):
        time = datetime.now().strftime("%Y%m%d-%H%M%S")       
        folder_name = f"TOWER_{time}"
        folder_path = os.path.join(os.getcwd(), "TowerUniverse",folder_name)
        img_path = os.path.join(folder_path,"imgs")
        os.makedirs(folder_path)
        os.makedirs(img_path)
        return folder_path
        
    def save_dg_fig(self, fig_name:int, graph:nx.DiGraph, path: str = "None") -> None:     
        if path=="None":
            path = f"{self.dungeon_folder}/imgs"           
        pos = nx.planar_layout(graph)
        plt.figure()
        nx.draw(G=graph, pos=pos, with_labels=True, node_color="red", node_size=500)
        file_path = os.path.join(path, f"{fig_name}.png")
        plt.savefig(file_path) 
        nx.write_graphml(graph, os.path.join(path,f"{fig_name}.graphml"))        
        
    def initiate_dungeon(self) -> nx.DiGraph:
        self.dungeon_folder = self.create_dungeon_folder()
        graph = nx.DiGraph()
        graph.add_node("EN:1", type="initial_room")
        self.save_dg_fig(fig_name="initial_dungeon",graph=graph)
        return graph
    
    def dice_roller(self, rolls:int, sides:int):
        value = 0        
        for _ in range(rolls):
            value += rd.randint(1,sides)
        return value
    
    def dungeon_rooms_loop(self, iterations:int, dungeon:nx.DiGraph, max_iterations=5) -> nx.DiGraph:
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
    
    def bfs(self, graph:nx.DiGraph) -> list[list[str]]:
        """Does BFS in the graph and returns a list of nodes for each lvl."""
        queue = []
        next_queue = []
        lvls = []
        current_lvl = []
        
        queue.append("EN:1")
        while len(queue)>0:
            current_node = queue.pop(0)
            current_lvl.append(current_node)         
            neighbors = list(nx.neighbors(graph,current_node))
            next_queue.extend(neighbors)
            
            if len(queue)==0:
                queue = next_queue.copy()
                lvls.append(current_lvl)
                current_lvl = []
                next_queue = []
        return lvls             
    
    def layout_loop(self, max_room_iter:int=15,room_dice:list[int]=[2,2]) -> nx.DiGraph:
        """_Creates the dungeon layout of rooms_

        Args:
            max_room_iter (int, optional): _iterations number of room creation loop_. Defaults to 15.
            room_dice (list[int], optional): _[diceRolls,diceSide]_. Defaults to [2,2].

        Returns:
            nx.DiGraph: _layout graph_
        """
        # creates root node
        dungeon = self.initiate_dungeon()  
        
        #apply first rule to initial node
        start_dungeon = self.grammar.apply_rule(target_hook="EN:1",graph=dungeon,rule=self.grammar.rules[0])
        self.save_dg_fig(fig_name="iter 1",graph=start_dungeon)
                
        #dungeon rooms loop
        #---apply rule 1 a number of times for all nodes in graph:
        times = self.dice_roller(rolls=room_dice[0], sides=room_dice[1])
        dungeon = self.dungeon_rooms_loop(iterations=times, dungeon=start_dungeon, max_iterations=max_room_iter)
        self.save_dg_fig(fig_name="final_dungeon",graph=dungeon, path=self.dungeon_folder)        
        return dungeon        
                        
    def chose_exit(self, graph:nx.DiGraph, start_lvl:int=0) -> str:
        """_Choses an exit for the dungeon based on a given minimum lvl of the tree_

        Args:
            graph (nx.DiGraph): _dungeon graph_
            start_lvl (int, optional): _minimum tree lvl, starting from 0_. Defaults to 3.
            
        Returns:
            : _transformed graph with exit node_
        """
        lvls = self.bfs(graph=graph)
        options = []
        for sublist in lvls[start_lvl:]:
            options.extend(sublist)
        graph.add_node("EX:1", type="room", isHook=bool("true"))
        graph.add_edge(rd.choice(options),"EX:1",type="connection",status="locked")
        return graph                
    
    def mission_graph(self, layout:nx.DiGraph) -> list[nx.DiGraph]:
        """Creates the mission graph, given the layou graph with an exit.

        Args:
            layout (nx.DiGraph): layout graph with an "EX" node.

        Returns:
            list[nx.DiGraph]: 
                [0]: modified layout graph
                [1]: mission graph
        """
        dungeon = layout
        mission_graph = nx.DiGraph()
        mission_graph.add_node("EX:1", type="room", isHook=bool("true"))
        
        #Apply mission grammar rule
        #To apply mission grammar rule, need to have available nodes to check
        #Build 
        
        return [dungeon, mission_graph]
        
    
        
        
    ################################
    ##### DUNGEON CREATION LOOP ####
    #TODO: NEED TO MAKE A COLOR MAP FOR THE GRAPH BASED ON NODE AND EDGE TYPES
    #TODO: RED FOR LOCKED EDGES, GREEN FOR FREE ONES
    #TODO: RED FOR LOCKED NODES, GREEN FOR FREE ONES
    def create_dungeon(self, layout_address:str = "None") -> nx.DiGraph:
        """_Creates the wizzard tower_

        Args:
            layout (nx.DiGraph, optional): A layout may be given, if not it creates one. Defaults to nx.DiGraph.

        Returns:
            nx.DiGraph: _wizard tower_
        """
        if layout_address=="None": 
            layout = self.layout_loop(max_room_iter=15,room_dice=[2,2])  
        else:
            layout = self.read_layout_from_file(graphml_file=layout_address)
            
        layout = self.chose_exit(graph=layout, start_lvl=0) 
        dungeon, mission_graph = self.mission_graph(layout=layout)
        
        #check progress
        layout = self.fill_color_map(graph=layout)
        mission_graph = self.fill_color_map(graph=mission_graph)
        dungeon = self.fill_color_map(graph=dungeon)
        self.grammar.draw_graph([["Layout",layout],["Mission",mission_graph],["Dungeon",dungeon]])       
        
    

        
        

if __name__ == "__main__":
    dungeon = WizarDDungeon(grammar_file="graph_productions.json")
    dungeon.create_dungeon(layout_address="TowerUniverse/TOWER_20240403-174325/final_dungeon.graphml")
    #dungeon.create_dungeon()
    