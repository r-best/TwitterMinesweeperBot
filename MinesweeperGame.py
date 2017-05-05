from random import randint


class Tile:
    count = 0  # Number of mines bordering the tile. M if the tile is a mine
    visible = False  # Whether the tile has been clicked on yet or not


class MinesweeperGame:
    height = None
    width = None
    mines = None  # 2D array of Tile objects

    def print_board(self):
        string = ""
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.mines[i][j].visible:
                    string += str(self.mines[i][j].count)
                else:
                    string += "\u220E"
                if j < self.width-1:
                    string += " "
            if i < self.height-1:
                string += "\n"
        return string

    def click_tile(self, i, j):
        self.mines[i-1][j-1].visible = True
        if self.mines[i-1][j-1].count == 'M':
            return False
        else:
            return True

    def create_board(self, num_mines):
        # Initialize the board with blank tiles
        self.mines = [[Tile() for j in range(0, self.width)] for i in range(0, self.height)]
        # Set some tiles to mines randomly
        for k in range(0, num_mines):
            while True:  # Keep generating random tile positions until you get one that isn't already a mine
                i = randint(0, self.height-1)
                j = randint(0, self.width-1)
                if self.mines[i][j].count != 'M':
                    break
            # Set the randomly selected tile to a mine
            self.mines[i][j].count = 'M'
            # Increment the counts of the tiles around the new mine
            for m in range(max(0, i-1), min(i+2, self.height)):
                for n in range(max(0, j-1), min(j+2, self.width)):
                    if (m != i or n != j) and self.mines[m][n].count != 'M':
                        self.mines[m][n].count += 1

    def __init__(self, board_height=6, board_width=6, num_mines=7):
        self.height = board_height
        self.width = board_width
        self.create_board(num_mines)

game = MinesweeperGame()
game.__init__()
game.click_tile(1, 1)
game.click_tile(1, 2)
game.click_tile(3, 5)
game.click_tile(2, 4)
game.click_tile(6, 1)
game.click_tile(5, 2)
print(game.print_board())
