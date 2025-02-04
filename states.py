import pickle
from board import Board

def all_possible_moves(states, player):
  newstates = []
  for state in states:
    is_term = Board(state).check_terminal()
    if is_term is None:
      for idx, ch in enumerate(state):
        if ch == ' ':
          newstate = state.copy()
          newstate[idx] = player
          newstates.append(newstate)
  return newstates

def get_distinct_tuples(tuple_list):
  string_set = set(map(str, tuple_list)) 
  distinct_tuples = [eval(s) for s in string_set]  
  return distinct_tuples

def save_states_to_file(states, filename):
    with open(filename, 'wb') as f:
        pickle.dump(states, f)

init_board = Board().state
states_0 = [init_board]
states_1 = all_possible_moves(states_0, 'O')
states_2 = all_possible_moves(states_1, 'X')
states_3 = all_possible_moves(states_2, 'O')
states_4 = all_possible_moves(states_3, 'X')
states_5 = all_possible_moves(states_4, 'O')
states_6 = all_possible_moves(states_5, 'X')
states_7 = all_possible_moves(states_6, 'O')
states_8 = all_possible_moves(states_7, 'X')
states_9 = all_possible_moves(states_8, 'O')

total_states = states_0 + states_1 + states_2 + states_3 + states_4 + states_5 + states_6 + states_7 + states_8 + states_9
distinct_states = get_distinct_tuples(total_states)

# Save the distinct_states list to a file
save_states_to_file(distinct_states, 'tictactoe_states.pkl')

if __name__ == '__main__':
    print(f"Found {len(distinct_states)} states")
