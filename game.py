from board import Board
from player import Player

class Game:
    def __init__(self, agentO, agentX):
        self.playerO = Player('O', agentO)
        self.playerX = Player('X', agentX)
        self.board = Board()
        self.current_player = None
        self.winner = None
        self.game_over = False

    def play(self):
        self.current_player = self.playerO
        while not self.game_over:
            move = self.current_player.move(self.board)
            self.board.state[move] = self.current_player.symbol
            self.game_over = self.check_game_over()
            self.current_player = self.playerO if self.current_player == self.playerX else self.playerX

    def check_game_over(self):
        game_status = self.board.check_terminal()
        if game_status is None:
            return False
        if game_status == 1:
            self.winner = self.playerO
        elif game_status == -1:
            self.winner = self.playerX
        return True
