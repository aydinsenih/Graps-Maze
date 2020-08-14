from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
map_file = "maps/test_loop.txt"
#map_file = "maps/test_loop_fork.txt"
#map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []


class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

visited = {}

def reverse(d):
    if d == "w":
        return "e"
    if d == "n":
        return "s"
    if d == "s":
        return "n"
    if d == "e":
        return "w"
    if d == None:
        return None
    
    

def path(roomID,cameFrom = None):
    stack = Stack()
    for direction in player.current_room.get_exits():
        #if player.current_room.get_room_in_direction(direction).id not in visited:
        if cameFrom != None:
            if player.current_room.get_room_in_direction(direction).id != player.current_room.get_room_in_direction(reverse(cameFrom)).id:
                stack.push(direction)
        else:
            stack.push(direction)

    if player.current_room.id not in visited:
        visited[player.current_room.id] = True
        if(cameFrom != None):
            traversal_path.append(cameFrom)

        while stack.size() != 0:
                goto = stack.pop()
                if player.current_room.get_room_in_direction(goto).id not in visited:#yollardaki loop sorununu cozen if
                    player.travel(goto)
                    path(player.current_room.id,goto)
            
            
        if(cameFrom != None):
            if len(visited) == len(world.rooms):
                return traversal_path
            player.travel(reverse(cameFrom))
            traversal_path.append(reverse(cameFrom))

print(path(0,))
print(traversal_path)


# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")



#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")


