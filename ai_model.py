import numpy as np
from collections import defaultdict
import math
import game
import copy
import random

class MCTS:
    def __init__(self, state, parent=None):
        self.state = copy.deepcopy(state)
        self.parent = parent
        self.children = []
        self.visits = 0
        self.reward = 0
        self.game_over = False
        self.untried_moves = self.get_possible_moves(self.state)
    
    def get_possible_moves(self,state):
        moves = []
        for x, row in enumerate(state['board']):
            for y, _ in enumerate(row):
                if state['board'][x][y] == game.game_class['empty']:
                    moves.append((x, y))
        return moves

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0
    
    def best_child(self, exploration_weight=1.4):
        return max(self.children, key=lambda node: node.uct_value(exploration_weight))
    
    def uct_value(self, exploration_weight):
        if self.visits == 0:
            return math.inf
        else:
            return self.reward / self.visits + exploration_weight * math.sqrt(
                math.log(self.parent.visits) / self.visits)
    
    def select(self):
        current = self
        while not current.is_terminal() and current.is_fully_expanded():
            if current.children:
                current = current.best_child()
            else:
                current = current.expand()
        return current
    
    def expand(self):
        if len(self.untried_moves) == 0:
            return None

        action = self.untried_moves.pop()
        new_state = copy.deepcopy(self.state)
        new_state['board'][action[0]][action[1]] = self.state['current_player']  # AI always plays 'O'
        child_node = MCTS(new_state, parent=self)
        self.children.append(child_node)
        return child_node

    def simulate(self):
        state = copy.deepcopy(self.state)
        current_player = 'O' if self.state['current_player'] == 'X' else 'X'  # Start with 'X' (user) since AI just played 'O'
        while not self.is_terminal(state):
            possible_moves = self.get_possible_moves(state)
            if not possible_moves:
                break
            action = random.choice(possible_moves)
            state['board'][action[0]][action[1]] = current_player
            current_player = 'O' if current_player == 'X' else 'X'  # Alternate players
        return self.get_result(state)

    def backpropagate(self, result):
        self.visits += 1
        self.reward += result
        if self.parent:
            self.parent.backpropagate(result)

    def is_terminal(self, state=None):
        if state is None:
            state = self.state
        if game.check_winner(state) or game.full_board(state):
            self.game_over = True
            return True
        return False

    def get_result(self, state):
        winner = game.check_winner(state)
        if winner == game.game_class['player']: ## here the AI loses
            return -1
        elif winner==game.game_class['opponent']:
            return 1
        else:
            return 0  # Draw

def mcts_decision(root_state, iterations=1000):
    root = MCTS(root_state)
    for _ in range(iterations):
        node = root.select()
        if not node.is_terminal():
            node = node.expand()
        result = node.simulate()
        node.backpropagate(result)
    return root.best_child(exploration_weight=2).state

# Example usage
