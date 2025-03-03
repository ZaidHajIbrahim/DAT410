import numpy as np
from collections import defaultdict


class MCTS:
    def __init__(self,state, parent=None, player = 'O'):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0
        self.player = player
        self.untried_actions = self.state.get_possible_actions()

