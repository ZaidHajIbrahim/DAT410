import numpy as np
from collections import defaultdict
import math


class MCTS:
    def __init__(self,state, parent=None, player = 'O'):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0
        self.player = player
        self.untried_actions = self.state.get_possible_actions()
    
    def is_fully_expanded(self):
        return len(self._untried_actions) == 0
    
    def best_child(self, exploration_weight=1.4):
        return max(self.children, key=lambda node: node.uct_value(exploration_weight))
    
    def uct_value(self, exploration_weight):
        if self.visits == 0:
            return math.inf
        return self.reward / self.visits + exploration_weight * math.sqrt(
                math.log(self.parent.visits) / self.visits)
    
    def select(self):
        current = self
        while not current.state.is_terminal() and not current.is_fully_expanded():
            if current.children:
                current = current.best_child()
            else:
                current = current.expand()
        return current
    
    def expand(self):
	
    action = self._untried_actions.pop()
    next_state = self.state.move(action)
    child_node = MonteCarloTreeSearchNode(
		next_state, parent=self, parent_action=action)

    self.children.append(child_node)
    return child_node 