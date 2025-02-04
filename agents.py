import random
import pickle
import numpy as np
from abc import ABC, abstractmethod
from board import Board, init_board
from states import all_possible_moves

class Agent(ABC):
    @abstractmethod
    def move(self, board):
        pass

class QLearnAgent(Agent):
    def __init__(self, player_symb):
        self.symb = player_symb
        self.state_space = build_state_space(player_symb)

    def move(self, board):
        state = tuple(board.state)
        max_q_value_idx = max(self.state_space[state]['q_values'])
        next_state_idx = self.state_space[state]['q_values'].index(max_q_value_idx)
        next_state = self.state_space[state]['next_states'][next_state_idx]

        return [i for i in range(9) if state[i] != next_state[i]][0]

    def move_policy(self, state, epsilon):
        """epsilon greedy policy"""
        if random.random() < epsilon:
            return random.choice(range(len(state['q_values'])))
        else:
            return state['q_values'].index(max(state['q_values']))

    def update_policy(self, state, qmax, action_idx, reward, alpha, gamma):
        """sarsamax update"""
        state['q_values'][action_idx] += alpha * (reward + gamma * qmax - state['q_values'][action_idx])

    def train(self, iters=10000000, initial_eps=1.0, min_eps=0.1, eps_decay=0.00005, alpha=0.2, gamma=0.9):
        for iteration in range(iters):
            eps = max(min_eps, initial_eps * np.exp(-eps_decay * iteration))
            curr_state = tuple(init_board)
            if iteration % 100000 == 0: print(f"Iteration: {iteration}")

            # Play a game
            while not self.state_space[curr_state]['is_terminal']:
                actions = self.state_space[curr_state]['next_states']
                q_values = self.state_space[curr_state]['q_values']

                # Epsilon-greedy action selection
                action_idx = self.move_policy(self.state_space[curr_state], eps)
                action_state = actions[action_idx]

                # Observe the reward from taking the action (i.e. reaching action_state)
                reward = self.state_space[action_state]['reward']
                
                # If the state after the agent's move is not terminal,
                # simulate the opponent's random move.
                if not self.state_space[action_state]['is_terminal']:
                    # Opponent's turn: choose a random move from action_state's next states
                    env_state = random.choice(self.state_space[action_state]['next_states'])
                    # Compute the max Q-value from the state after the opponent's move.
                    if not self.state_space[env_state]['is_terminal']:
                        qmax = np.max(self.state_space[env_state]['q_values'])
                    else:
                        qmax = 0.0
                else:
                    env_state = action_state
                    qmax = 0.0

                # Q-learning update:
                self.update_policy(self.state_space[curr_state], qmax, action_idx, reward, alpha, gamma)
                
                # Transition to the new state (after the opponent's move, if applicable)
                curr_state = env_state

    def save(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.state_space, f)

    def load(self, filename):
        with open(filename, 'rb') as f:
            self.state_space = pickle.load(f)

class RandomAgent(Agent):
    def move(self, board):
        return random.choice([i for i, x in enumerate(board.state) if x == ' '])

class ManualAgent(Agent):
    def move(self, board):
        board.print_board()
        move = int(input('Enter move: '))
        return move

def build_state_space(player_symb):
    def load_states_from_file(filename):
        with open(filename, 'rb') as f:
            states = pickle.load(f)
        return states
    # Load the states list from the file
    states = load_states_from_file('tictactoe_states.pkl')

    # Build the state space (using only legal, reachable states)
    state_space = {}

    for state in states:
        board = Board(state)
        state_tuple = tuple(state)
        is_term = board.check_terminal()
        win_num = 1 if player_symb == 'O' else -1

        # Reward: +1 if agent wins, -1 if opponent wins, 0 otherwise
        reward = 1 if is_term == win_num else (-1 if win_num == -1 else 0)

        if is_term is not None:
            next_states = []
        else:
            # Determine whose move it is: if counts are equal then it's X's turn; otherwise, it's O's turn.
            if state.count('X') == state.count('O'):
                next_states = list(map(tuple, all_possible_moves([state], 'O')))
            else:
                next_states = list(map(tuple, all_possible_moves([state], 'X')))
                
        state_space[state_tuple] = {
            'is_terminal': False if is_term is None else True,
            'reward': reward,
            'next_states': next_states,
        }
        # Initialize Q-values for each available action in this state
        state_space[state_tuple]['q_values'] = [0.0] * len(next_states)
    return state_space
