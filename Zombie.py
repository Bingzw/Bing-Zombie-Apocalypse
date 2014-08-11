"""
Student portion of Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = "obstacle"
HUMAN = "human"
ZOMBIE = "zombie"


class Zombie(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        self._grid_height = grid_height
        self._grid_width = grid_width
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
                
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)       
          
    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        idx = 0
        while idx < len(self._zombie_list):
          yield self._zombie_list[idx]
          idx = idx + 1

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list) 
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        idx = 0
        while idx < len(self._human_list):
          yield self._human_list[idx]
          idx = idx + 1
        
    def compute_distance_field(self, entity_type):
        """
        Function computes a 2D distance field
        Distance at member of entity_queue is zero
        Shortest paths avoid obstacles and use distance_type distances
        """
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        distance_field = [[self._grid_height * self._grid_width for dummy_col in range(self._grid_width)] 
                       for dummy_row in range(self._grid_height)]
        boundary = poc_queue.Queue()
        if entity_type == HUMAN:
            entity_list = self._human_list
        elif entity_type == ZOMBIE:
            entity_list = self._zombie_list
        for entity in entity_list:
            boundary.enqueue(entity)
            visited.set_full(entity[0], entity[1])
            distance_field[entity[0]][entity[1]] = 0
        while boundary.__len__() != 0:
            current_cell = boundary.dequeue()
            if entity_type == HUMAN:
                all_neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            elif entity_type == ZOMBIE:
                all_neighbors = self.four_neighbors(current_cell[0], current_cell[1])
            for neighbor_cell in all_neighbors:
                if visited.is_empty(neighbor_cell[0], neighbor_cell[1]) == True and self.is_empty(neighbor_cell[0], neighbor_cell[1]) == True:
                    visited.set_full(neighbor_cell[0], neighbor_cell[1])
                    boundary.enqueue(neighbor_cell)
                    distance_field[neighbor_cell[0]][neighbor_cell[1]] = min(distance_field[neighbor_cell[0]][neighbor_cell[1]], distance_field[current_cell[0]][current_cell[1]] + 1)
        return distance_field

         
        
    def move_humans(self, zombie_distance):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        new_human_list = []
        for human in self._human_list:
            human_all_neighbors = self.eight_neighbors(human[0], human[1])
            max_distance = zombie_distance[human[0]][human[1]]
            max_row = human[0]
            max_col = human[1]
            for human_neighbor in human_all_neighbors:
                if zombie_distance[human_neighbor[0]][human_neighbor[1]] >= max_distance and self.is_empty(human_neighbor[0], human_neighbor[1]) == True:
                    max_distance = zombie_distance[human_neighbor[0]][human_neighbor[1]]
                    max_row, max_col = human_neighbor[0], human_neighbor[1]
            new_human_list.append((max_row, max_col))
        self._human_list = new_human_list 
                
        
    def move_zombies(self, human_distance):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        new_zombie_list = []
        for zombie in self._zombie_list:
            zombie_all_neighbors = self.four_neighbors(zombie[0], zombie[1])
            min_distance = human_distance[zombie[0]][zombie[1]]
            min_row = zombie[0]
            min_col = zombie[1]
            for zombie_neighbor in zombie_all_neighbors:
                if human_distance[zombie_neighbor[0]][zombie_neighbor[1]] <= min_distance and self.is_empty(zombie_neighbor[0], zombie_neighbor[1]) == True:
                    min_distance = human_distance[zombie_neighbor[0]][zombie_neighbor[1]]
                    min_row, min_col = zombie_neighbor[0], zombie_neighbor[1]
            new_zombie_list.append((min_row, min_col))
        self._zombie_list = new_zombie_list 

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

a = Zombie(3, 3, [], [], [(2, 2)])
a.compute_distance_field(HUMAN)
poc_zombie_gui.run_gui(Zombie(30, 40))
