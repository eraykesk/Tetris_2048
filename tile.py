import lib.stddraw as stddraw  # stddraw is used as a basic graphics library
from lib.color import Color  # used for coloring the tile and the number on it

# Class used for modeling numbered tiles as in 2048
class Tile: 
   # Class attributes shared among all Tile objects
   # ---------------------------------------------------------------------------
   # the value of the boundary thickness (for the boxes around the tiles)
   boundary_thickness = 0.004
   # font family and size used for displaying the tile number
   font_family, font_size = "Arial", 14

   # Constructor that creates a tile with 2 as the number on it
   def __init__(self):
     # set the number on the tile
        self.number_arr = {2, 4}
        self.number = random.choice(tuple(self.number_arr))
        # set the colors of the tile depending on the number
        if self.number == 2:
            self.background_color = Color(205,105,201)

        if self.number == 4:
            self.background_color = Color(238,0,0)

        if self.number == 8:
            self.background_color = Color(238,238,0)

        if self.number == 16:
            self.background_color = Color(99,184,255)

        if self.number == 32:
            self.background_color = Color(84,139,84)

        if self.number == 64:
            self.background_color = Color(208,32,144)

        if self.number == 128:
            self.background_color = Color(255,99,71)

        if self.number == 256:
            self.background_color = Color(0,199,140)

        if self.number == 512:
            self.background_color = Color(155,48,255)

        if self.number == 1024:
            self.background_color = Color(176,224,230)

        if self.number == 2048:
            self.background_color = Color(85,26,139)

      
      self.foreground_color = Color(0, 100, 200) # foreground (number) color
      self.box_color = Color(0, 100, 200) # box (boundary) color

   # Method for drawing the tile
   def draw(self, position, length = 1):
      # draw the tile as a filled square
      stddraw.setPenColor(self.background_color)
      stddraw.filledSquare(position.x, position.y, length / 2)
      # draw the bounding box around the tile as a square
      stddraw.setPenColor(self.box_color)
      stddraw.setPenRadius(Tile.boundary_thickness)
      stddraw.square(position.x, position.y, length / 2)
      stddraw.setPenRadius()  # reset the pen radius to its default value
      # draw the number on the tile
      stddraw.setPenColor(self.foreground_color)
      stddraw.setFontFamily(Tile.font_family)
      stddraw.setFontSize(Tile.font_size)
      stddraw.text(position.x, position.y, str(self.number))
