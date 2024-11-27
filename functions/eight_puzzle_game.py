import random

class PuzzleGame:
    def __init__(self):
        self.board = self.create_board()

    def create_board(self):
        board = list(range(9))
        random.shuffle(board)
        return board

    def print_board(self):
        print("\nCurrent Puzzle State:")
        for i in range(0, 9, 3):
            print(self.board[i:i + 3])
        print()

    def is_solved(self):
        return self.board == list(range(9))

    def move(self, tile):
        empty_pos = self.board.index(0)
        tile_pos = self.board.index(tile)

        if tile_pos in [empty_pos - 1, empty_pos + 1, empty_pos - 3, empty_pos + 3]:
            self.board[empty_pos], self.board[tile_pos] = self.board[tile_pos], self.board[empty_pos]
            return True
        return False

def play_game():
    game = PuzzleGame()
    while not game.is_solved():
        game.print_board()
        move = int(input("Enter the tile number to move (1-8): "))
        if not game.move(move):
            print("Invalid move! Try again.")
    
    game.print_board()
    print("Congratulations, you've solved the puzzle!")

