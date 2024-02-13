import numpy as np
class Node:
    def __init__(self, game, args, state, parent=None, action_taken=None):
        self.game = game
        self.args = args
        self.state = state
        self.parent = parent
        self.action_taken = action_taken

        self.children = [] # all the children of this node
        self.expandable_moves = game.get_valid_moves(state) # all the valid moves I can take from this state
 
        self.visit_count = 0 # number of times the node is visited
        self.value_sum = 0 # number of wins when I take this node

    def fullyExpanded(self): # to check whether all the moves in the node has been visited
        pass

    def select(self): # select down selection
        # calculated ucb score for each child and select the node with the highest UCB score
        best_child = None
        best_ucb = -np.inf

        for child in self.children:
            ucb = self.get_ucb(child) # 
            if ucb> best_ucb:
                best_child = child
                best_ucb = ucb

        return best_child

    def get_ucb(self, child):
        q_value = 1 - (child.value_sum / child.visit_count) # child.value_sum is the value perceived by the child (child is the opponent player!)
        return  q_value + self.args['c']*np.sqrt(np.log((self.visit_count/child.visit_count)))



class MCTS:
    def __init__(self, game, args):
        self.game = game
        self.args = args

    
    
    def search(self, state):
        root = Node(self.game, self.args, state) # initialises root node
        for search in range(self.args['num_searches']):
            node = root
            # SELECTION
            # keep selecting all the nodes
            while node.fullyExpanded():
                node = node.select()
            
            value, termination = self.game.get_value_and_termination(node.state, node.action_taken)
            # EXPANSION
            # SIMULATION
            # BACKPROPOGATION

        # return visit_counts
