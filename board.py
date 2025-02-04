class Board:
    def __init__(self, state=None):
        if state is not None:
            self.state = state
        else:
            self.state = [' '] * 9

    def print_board(self):
        print(self.state[0] + ' | ' + self.state[1] + ' | ' + self.state[2])
        print('--+---+--')
        print(self.state[3] + ' | ' + self.state[4] + ' | ' + self.state[5])
        print('--+---+--')
        print(self.state[6] + ' | ' + self.state[7] + ' | ' + self.state[8])

    def check_terminal(self):
        """
        Returns 
        1 if player O wins, 
        -1 if player X wins, 
        0 if draw, 
        None if game is not over
        """
        for idxs in [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]:
            if self.state[idxs[0]] == self.state[idxs[1]] == self.state[idxs[2]] != ' ':
                if self.state[idxs[0]] == 'O':
                    return 1
                else:
                    return -1
        if self.state.count(' ') == 0:
            return 0
        return None

init_board = Board().state