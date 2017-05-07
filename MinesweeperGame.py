from random import randint


class Tile:
    count = 0  # Number of mines bordering the tile. M if the tile is a mine
    visible = False  # Whether the tile has been clicked on yet or not


class MinesweeperGame:
    height = None
    width = None
    mines = None  # 2D array of Tile objects

    def mines_to_string(self):
        # Used to convert the board to a string format for storage
        string = ""
        for i in range(0, self.height):
            for j in range(0, self.width):
                if self.mines[i][j].visible:
                    string += str(self.mines[i][j].count)
                elif not self.mines[i][j].visible:
                    if self.mines[i][j].count == 'M':
                        string += "N"
                    else:
                        string += '-' + str(self.mines[i][j].count)
                if j < self.height-1:
                    string += " "
            if i < self.width-1:
                string += "\n"
        return string

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

    def uncover_surroundings(self, I, J):
        # That thing that happens when you click a 0 tile and it uncovers all the connected 0 tiles
        # and you get a whole bunch of board at once if you're lucky
        self.mines[I][J].visible = True
        for i in range(max(0, I-1), min(I+1, self.height-1)+1):
            for j in range(max(0, J-1), min(J+1, self.width-1)+1):
                if i != I or j != J:
                    if self.mines[i][j].count == 0 and not self.mines[i][j].visible:
                        self.uncover_surroundings(i, j)
                    self.mines[i][j].visible = True

    def click_tile(self, j, i):
        self.mines[i-1][j-1].visible = True
        if self.mines[i-1][j-1].count == 'M':
            return False
        else:
            if self.mines[i-1][j-1].count == 0:
                self.uncover_surroundings(i-1, j-1)
            return True

    def create_new_board(self, num_mines):
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

    def load_board(self, board_string):
        board_rows = board_string.split('\n')
        for i in range(0, board_rows.__len__()):
            board_columns = board_rows[i].split(' ')
            for j in range(0, board_columns.__len__()):
                self.mines[i][j] = Tile()
                if board_columns[j] == 'M':
                    self.mines[i][j].count = 'M'
                    self.mines[i][j].visible = True
                elif board_columns[j] == 'N':
                    self.mines[i][j].count = 'M'
                    self.mines[i][j].visible = False
                elif '-' in board_columns[j]:
                    self.mines[i][j].count = int(board_columns[j]) * -1
                    self.mines[i][j].visible = False
                else:
                    self.mines[i][j].count = int(board_columns[j])
                    self.mines[i][j].visible = True

    def __init__(self, board_height=6, board_width=6, num_mines=7):
        self.height = board_height
        self.width = board_width
        if num_mines != -1:
            self.create_new_board(num_mines)
