
from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource
import heapq

#TODO: fix resource amoutn

move_priority =  { 'Up': 0, 'Down':1, 'Left':2,  'Right':3, 'Initial':-1 }


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)


    def move_helper(self, cant_move_at, offset, action):

        old_config = list(self.config)
        index_of_blank = old_config.index(0)


        if index_of_blank in cant_move_at: return None
        swap_index = index_of_blank + offset


        # print(old_config)
        # print("to")

        #preform the swap
        old_config[index_of_blank] = old_config[swap_index]
        old_config[swap_index] = 0

        #print(old_config)

        path = str(self.action)
        path += " " + action

        new_state = PuzzleState(old_config, self.n, self, action, self.cost + 1)
        return new_state


    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        new_state = self.move_helper([0,1,2],-3,'Up')
        return new_state


    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        new_state = self.move_helper([6,7,8],3,'Down')
        return new_state

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        new_state = self.move_helper([0,3,6],-1,'Left')
        return new_state

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        new_state = self.move_helper([2,5,8],1,'Right')
        return new_state

    def expand(self):
        """ Generate the child nodes of this node """

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children


def getDepth(state):
    depth = 0
    while state.action != 'Initial':
        state = state.parent
        depth += 1
    return depth

def getPath(state):

    path = []
    while state.action != 'Initial':
        path.insert(0,state.action)
        state = state.parent
    return path

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(final_state, nodes_expanded,lastExpored,timeElapsed):
    ### Student Code Goes here
    print(f'path_to_goal: {getPath(final_state)}')
    print(f'cost_of_path: {final_state.cost}')
    print(f'nodes_expanded: {nodes_expanded}')
    print(f'search_depth: { final_state.cost}')
    print(f'max_search_depth: {lastExpored.cost}')
    print(f'running_time: {timeElapsed}')
    print(f'max_ram_usage: {resource.getrusage(resource.RUSAGE_SELF).ru_maxrss }')

def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###

    start_time  = time.time()
    frontier = Q.Queue()
    frontier.put(initial_state)

    in_frontier = set()
    in_frontier.add(tuple(initial_state.config))

    explored = set()
    lastExpored = initial_state

    while frontier.empty() == False:
        state = frontier.get()
        #in_frontier.discard(tuple(state.config))

        if test_goal(state):
            writeOutput(state,len(explored), lastExpored,time.time()-start_time)
            return True

        explored.add(tuple(state.config))

        for child in state.expand():
            if tuple(child.config) not in explored and tuple(child.config) not in in_frontier:
                frontier.put(child)
                in_frontier.add(tuple(child.config))
                lastExpored = child
    return False

def dfs_search(initial_state):

    start_time  = time.time()
    frontier = list()
    frontier.append(initial_state)


    in_frontier = set()
    in_frontier.add(tuple(initial_state.config))

    explored = set()
    lastExpored = initial_state

    while len(frontier) != 0:
        state = frontier.pop()
        #in_frontier.discard(tuple(state.config))

        if test_goal(state):
            writeOutput(state,len(explored), lastExpored,time.time()-start_time)
            return True

        explored.add(tuple(state.config))
        i = 0
        for child in state.expand():
            if tuple(child.config) not in explored and tuple(child.config) not in in_frontier:
                frontier.insert(len(frontier) - i ,child)
                i+=1
                in_frontier.add(tuple(child.config))
                lastExpored = child
    return False


def make_node(state):
    node = [calculate_total_cost(state), move_priority[state.action],time.time(),state]

    return node


def A_star_search(initial_state):
    """A * search"""

    start_time  = time.time()

    frontier = list()
    heapq.heapify(frontier)
    heapq.heappush(frontier,make_node(initial_state))



    in_frontier = set()
    in_frontier.add(tuple(initial_state.config))

    explored = set()
    lastExpored = initial_state

    while len(frontier) != 0:

        state = heapq.heappop(frontier)
        state_config = state[3].config
        #in_frontier.discard(tuple(state_config))

        if test_goal(state[3]):
            writeOutput(state[3],len(explored), lastExpored,time.time()-start_time)
            return True

        explored.add(tuple(state[3].config))

        for child in state[3].expand():
            if tuple(child.config) not in explored and tuple(child.config) not in in_frontier:
                heapq.heappush(frontier,make_node(child))
                in_frontier.add(tuple(child.config))
                lastExpored = child


    return False

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    cost_from_root = state.cost
    manhattan_cost = 0
    for x in range(len(state.config)):
        manhattan_cost += calculate_manhattan_dist(x,state.config[x],state.n)
    return manhattan_cost + cost_from_root


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    return abs((value % n) - (idx % n )) + abs((value // n) - (idx // n ))


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    ##TODO make this not hardcoded
    #print(puzzle_state.config)
    return puzzle_state.config == [0,1,2,3,4,5,6,7,8]


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()

    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()