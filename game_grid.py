import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the game grid
from point import Point  # used for tile positions
import numpy as np  # fundamental Python module for scientific computing


# Class used for modelling the game grid
class GameGrid:
    # Constructor for creating the game grid based on the given arguments
    def __init__(self, grid_h, grid_w):
        # set the dimensions of the game grid as the given arguments
        self.grid_height = grid_h
        self.grid_width = grid_w
        # score variable
        self.score = 0
        # create a tile matrix to store the tiles landed onto the game grid
        self.tile_matrix = np.full((grid_h, grid_w), None)
        # create the tetromino that is currently being moved on the game grid
        self.current_tetromino = None
        # the game_over flag shows whether the game is over or not
        self.game_over = False
        # set the color used for the empty grid cells
        self.empty_cell_color = Color(42, 69, 99)
        # set the colors used for the grid lines and the grid boundaries
        self.line_color = Color(0, 100, 200)
        self.boundary_color = Color(0, 100, 200)
        # thickness values used for the grid lines and the boundaries
        self.line_thickness = 0.002
        self.box_thickness = 10 * self.line_thickness

    # Method used for displaying the game grid
    def display(self):
        # clear the background to empty_cell_color
        stddraw.clear(self.empty_cell_color)
        # draw the game grid
        self.draw_grid()
        # draw the current/active tetromino if it is not None (the case when the
        # game grid is updated)
        if self.current_tetromino is not None:
            self.current_tetromino.draw()
        # draw a box around the game grid
        self.draw_boundaries()
        # show the resulting drawing with a pause duration = 250 ms
        stddraw.show(250)

    # Method for drawing the cells and the lines of the game grid
    def draw_grid(self):
        # for each cell of the game grid
        for row in range(self.grid_height):
            for col in range(self.grid_width):
                # draw the tile if the grid cell is occupied by a tile
                if self.tile_matrix[row][col] is not None:
                    self.tile_matrix[row][col].draw(Point(col, row))
        # draw the inner lines of the grid
        stddraw.setPenColor(self.line_color)
        stddraw.setPenRadius(self.line_thickness)
        # x and y ranges for the game grid
        start_x, end_x = -0.5, self.grid_width - 0.5
        start_y, end_y = -0.5, self.grid_height - 0.5
        for x in np.arange(start_x + 1, end_x, 1):  # vertical inner lines
            stddraw.line(x, start_y, x, end_y)
        for y in np.arange(start_y + 1, end_y, 1):  # horizontal inner lines
            stddraw.line(start_x, y, end_x, y)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method for drawing the boundaries around the game grid
    def draw_boundaries(self):
        # draw a bounding box around the game grid as a rectangle
        stddraw.setPenColor(self.boundary_color)  # using boundary_color
        # set the pen radius as box_thickness (half of this thickness is visible
        # for the bounding box as its lines lie on the boundaries of the canvas)
        stddraw.setPenRadius(self.box_thickness)
        # the coordinates of the bottom left corner of the game grid
        pos_x, pos_y = -0.5, -0.5
        stddraw.rectangle(pos_x, pos_y, self.grid_width, self.grid_height)
        stddraw.setPenRadius()  # reset the pen radius to its default value

    # Method used for checking whether the grid cell with given row and column
    # indexes is occupied by a tile or empty
    def is_occupied(self, row, col):
        # considering newly entered tetrominoes to the game grid that may have
        # tiles with position.y >= grid_height
        if not self.is_inside(row, col):
            return False
        # the cell is occupied by a tile if it is not None
        return self.tile_matrix[row][col] is not None

    # Method used for checking whether the cell with given row and column indexes
    # is inside the game grid or not
    def is_inside(self, row, col):
        if row < 0 or row >= self.grid_height:
            return False
        if col < 0 or col >= self.grid_width:
            return False
        return True

    # Method that locks the tiles of the landed tetromino on the game grid while
    # checking if the game is over due to having tiles above the topmost grid row.
    # The method returns True when the game is over and False otherwise.
    def update_grid(self, tiles_to_lock, blc_position):
        # necessary for the display method to stop displaying the tetromino
        self.current_tetromino = None
        # lock the tiles of the current tetromino (tiles_to_lock) on the game grid
        n_rows, n_cols = len(tiles_to_lock), len(tiles_to_lock[0])
        for col in range(n_cols):
            for row in range(n_rows):
                # place each tile onto the game grid
                if tiles_to_lock[row][col] is not None:
                    # compute the position of the tile on the game grid
                    pos = Point()
                    pos.x = blc_position.x + col
                    pos.y = blc_position.y + (n_rows - 1) - row
                    if self.is_inside(pos.y, pos.x):
                        self.tile_matrix[pos.y][pos.x] = tiles_to_lock[row][col]
                    # the game is over if any placed tile is above the game grid
                    else:
                        self.game_over = True

        # clearing fully occupied rows
        self.clear_full_lines()
        
        # merging tiles and updating colors
        self.merge_tiles()
        
        # deleting unconnected tiles
        self.delete_unconnected()

        # return the game_over flag
        return self.game_over

    # Method for clearing full horizontal lines on the game board
    # and computing score
    def clear_full_lines(self):
        # creating a new empty array to append the game board
        # after deleting the full line
        new_row = np.full((1, self.grid_width), None)
        # creating a temporary score variable
        temp_score = 0
        # loop for checking every row
        for i in range(len(self.tile_matrix)):
            # a boolean variable to check if tile is occupied
            isFull = True
            # loop for checking every column
            for j in range(len(self.tile_matrix[i])):
                # if cell is occupied isFull remains true and loop continues
                if self.is_occupied(i, j):
                    isFull = True
                    # adding the number of occupied tile to temp_score
                    temp_score += Tile.get_number(self.tile_matrix[i][j])
                # if cell is not occupied isFull is updated to false and inner loop breaks
                # and temp_score is updated to 0 to compute other lines score
                else:
                    isFull = False
                    temp_score == 0
                    break

            # if isFull is true after checking every cell in a row deleting the row
            # and adding a new empty row to game board
            # and adding temp_score to score variable
            if isFull == True:
                self.tile_matrix = np.delete(self.tile_matrix, i, 0)
                self.tile_matrix = np.append(self.tile_matrix, new_row, 0)
                self.score += temp_score
                print(self.score)

     # function to merge tiles with same number
     # and updating score
     def merge_tiles(self):
         # loop for checking every element until 2nd line to not get index out of bounds error
         for i in range(len(self.tile_matrix)-1):
             for k in range(0,len(self.tile_matrix[i])):
                 # checking if both tiles are occupied and have the same number
                 if self.is_occupied(i - 1, k) and self.is_occupied(i, k):
                     if Tile.get_number(self.tile_matrix[i][k]) == Tile.get_number(self.tile_matrix[i - 1][k]):
                         # updating the number of the lower tile
                         n = Tile.get_number(self.tile_matrix[i-1][k])
                         Tile.set_number(self.tile_matrix[i-1][k], n+n)
                         # deleting the upper tile
                         self.tile_matrix[i] = np.insert(np.delete(self.tile_matrix[i], k, 0), k, None)
                            
                         #updating the colors
                         Tile.update_color(self.tile_matrix[i-1][k])
                            
                         # updating the score
                         self.score += n+n
                            
    # a method for deleting unconnected tiles
    def delete_unconnected(self):
        # loop for checking every cell which is not at the border because they are connected to the borders
        for i in range(1,len(self.tile_matrix)-1):
            for j in range(1,len(self.tile_matrix[i])-1):
                # checking if the cell is occupied
                if self.is_occupied(i,j):
                    # checking is any of the cells neighbors are occupied
                    if not self.is_occupied(i+1,j) and not self.is_occupied(i,j-1) and not self.is_occupied(i,j+1) and not self.is_occupied(i-1,j):
                        # if they are not occupied adding the number of the tile to the score and deleting it
                        self.score += Tile.get_number(self.tile_matrix[i][j])
                        self.tile_matrix[i] = np.insert(np.delete(self.tile_matrix[i], j, 0), j, None)
