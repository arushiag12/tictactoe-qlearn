import pickle
from game import Game
from agents import RandomAgent, ManualAgent, QLearnAgent

RLplayer = QLearnAgent('O')
RLplayer.load('trained_qlearn_agent.pkl')

game = Game(RLplayer, ManualAgent())
game.play()
game.board.print_board()
print('Winner is', game.winner.symbol if game.winner else 'None')
