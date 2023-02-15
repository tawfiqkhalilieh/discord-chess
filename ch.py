import chess
import chess.engine
import chess.svg


class ChessGame:
    def __init__(self):
        self.board = chess.Board()
        self.render_game()
  
    def play(self) -> bool:
        engine = chess.engine.SimpleEngine.popen_uci(
            r"fish.exe")
        result = engine.play(self.board, chess.engine.Limit(time=0.1))
        self.board.push(result.move)
        engine.quit()

        self.render_game()
      
    def render_game(self):
      with open("games/chess5.svg", 'w') as file:
            if chess.svg.board:
                file.write(chess.svg.board(
                    self.board,
                    size=1000,
                ))
              
    def reset(self):
        self.board = chess.Board()