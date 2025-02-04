class Player:
    def __init__(self, symbol, agent):
        self.symbol = symbol
        self.agent = agent

    def move(self, board):
        return self.agent.move(board)
    
    def __str__(self):
        return f"Player {self.symbol}"