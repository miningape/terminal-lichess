# This class generates the initial positions and colors of pieces 
# And hanfle the moving of pieces around the board

# Helper import
import helper
import re

class ChessState:
  board = {'black': [], 'white': []}

  current_state = 'black'
  
  white_keymap = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
  black_keymap = ['h', 'g', 'f', 'e', 'd', 'c', 'b', 'a']

  white_kingHasMoved = False
  black_kingHasMoved = False

  def __init__(self):
    self.start("")

  def flip(self):
    if self.current_state == 'black':
      self.current_state = 'white'
    else:
      self.current_state = 'black'
  
  def setState( self, state ):
    if not state == 'random':
      self.current_state = state
  
  def cur_board(self):
    return self.board[self.current_state]

  def start(self, longStrMoves):
    self.board['black'] = self.place_pieces_black_perspective()
    copy_black_board = helper.shallow_2d_copy( self.board['black'] )
    self.board['white'] = helper.rotate( copy_black_board )
    
    for move in longStrMoves.split():
      self.make_move(move)

  def place_pieces_black_perspective(self):
    board = []
    count = 1

    for x in range(10):
      layer = []
      for y in range(10):
        if (x == 0 or x == 9):
          if (y > 0 and y < 9):
            cell = 'DI' + self.black_keymap[y-1]
          else:
            cell = 'NNN'
        elif (y == 0 or y == 9):
          if (x > 0 and x < 9):
            cell = 'DI{}'.format( x  )
        else:
          cell = 'B' if bool(count % 2) else 'W'
          count += 1

          if (x == 1 or x == 8):    # Back ranks
            if (y == 1 or y == 8):  # Rooks
              cell += 'R'

            elif (y == 2 or y == 7):  # Knights
              cell += 'N'
            
            elif (y == 3 or y == 6):  # Bishops
              cell += 'B'
            
            elif (y == 4):            # King
              cell += 'K'

            elif (y == 5):            # Queen
              cell += 'Q'
            
            cell += 'W' if (x == 1) else 'B'  # Color

          elif (x == 2 or x == 7):    # PAWN STORM
            cell += 'P'
            cell += 'W' if (x == 2) else 'B'  # Color
            
          else:
            cell += 'NN'         # Otherwise its empty      
        layer.append(cell)
      count -= 1
      board.append(layer)
    
    return board
  
  def make_move(self, move): # move: string(e1e2) => char int char int
    pattern = re.compile('([a-hA-H]{1,1})([0-9]{1,1})([a-hA-H]{1,1})([0-9]{1,1})(q|n|r|b)?')
    match = pattern.match(move)
    
    if not(match == None):
      # Castling code (could definately be refactored to be neater and less expensive, at the moment im just gonna leave it as is because it makes intuitive sense to me)
      # If we are selecting a square the king starts on
      if match.group(1) == 'e' and (match.group(2) == '1' or match.group(2) == '8'):
        # If the king is travelling 2 squares away horisonatally
        if (match.group(3) == 'g' or match.group(3) == 'c') and match.group(2) == match.group(4):
          # If the king we are looking at is white and has not mooved
          if match.group(2) == '1' and not self.white_kingHasMoved:
            if match.group(3) == 'g':   # Are we moving to the left or right
              self.make_move('h1f1')    # Move white left rook
            else:
              self.make_move('a1d1')    # Move white right rook
          elif not self.black_kingHasMoved: # If black hasnt move king yet
            if match.group(3) == 'g':   # Are we moving left or right
              self.make_move('h8f8')  
            else:
              self.make_move('a8d8')
        
        # No matter what the first time we accees this square it will have a king on it so, it will have "moved"
        if match.group(2) == '1':
          self.white_kingHasMoved = True
        else:
          self.black_kingHasMoved = True

      # We replicate it(~20 instructions) because it is much less than rotating(>100 instructions)
      if match.group(5) is not None:    # If we are promoting
        print(match.group(5))
        self.moveBlack( match, promotion=match.group(5) )
        self.moveWhite( match, promotion=match.group(5) )
      else:
        self.moveBlack( match )
        self.moveWhite( match )
    else:
      # Could throw an error, right now i dont wanna see that ugliness, so ill leave it as print
      print('YOU TRIED TO MOVE {}, but it couldnt match, try without spaces where the format for a square is (letter, number) and the format for the move is (square from, square to)'.format(move))
  
  # for black the letters are inverted
  def moveBlack(self, match, promotion=None):
    # Extract data from capturing groups
    sqFrom = {'char': match.group(1), 'num': match.group(2)}
    sqTo   = {'char': match.group(3), 'num': match.group(4)}

    # Find/format coords (:Row     ,             :Column)
    coordFrom = (int(sqFrom['num']), self.black_keymap.index(sqFrom['char']) + 1) # Order is inverted with black_keymap
    coordTo   = (int(sqTo['num']), self.black_keymap.index(sqTo['char']) + 1)

    # When a piece moves, the square it left is empty, but the squares color is the same
    fromCell = self.board['black'][coordFrom[0]][coordFrom[1]]
    replaceFromCell = "{}NN".format(fromCell[:1])                           # Extract the color of the cell but erase pieces
    toCellColor = self.board['black'][coordTo[0]][coordTo[1]][:1]           # Extract color
    toCellPiece = fromCell[1:] if promotion == None else promotion.upper() + fromCell[2:]       # Extract the piece
    replaceToCell = "{}{}".format(toCellColor, toCellPiece)                 # Combine extracted piece & color

    # Perform replacements
    self.board['black'][coordFrom[0]][coordFrom[1]] = replaceFromCell
    self.board['black'][coordTo[0]][coordTo[1]]     = replaceToCell
    

  # for white numbers are intverted 
  def moveWhite(self, match, promotion=None):
    # Extract data from capturing groups
    sqFrom = {'char': match.group(1), 'num': match.group(2)}
    sqTo   = {'char': match.group(3), 'num': match.group(4)}

    # Find/format coords (:Row     ,             :Column)
    coordFrom = (9 - int(sqFrom['num']), self.white_keymap.index(sqFrom['char']) + 1) # 9 - coord is to reverse it
    coordTo   = (9 - int(sqTo['num']), self.white_keymap.index(sqTo['char']) + 1)

    # When a piece moves, the square it left is empty, but the squares color is the same
    fromCell = self.board['white'][coordFrom[0]][coordFrom[1]]
    replaceFromCell = "{}NN".format(fromCell[:1]) # Extract the color of the cell but erase pieces
    toCellColor = self.board['white'][coordTo[0]][coordTo[1]][:1]             # Extract color
    toCellPiece = fromCell[1:] if promotion == None else promotion.upper() + fromCell[2:]           # Extract the piece
    replaceToCell = "{}{}".format(toCellColor, toCellPiece)                   # Combine extracted piece & color

    # Perform replacements
    self.board['white'][coordFrom[0]][coordFrom[1]] = replaceFromCell
    self.board['white'][coordTo[0]][coordTo[1]]     = replaceToCell


if __name__ == '__main__':
  gboard = ChessState()
  #print(gboard.board['white'])
  print(gboard.board['white'])
  print(gboard.start('e2e4 c7c5 f2f4 d7d6 g1f3 b8c6 f1c4 g8f6 d2d3 g7g6 e1g1 f8g7'))
  print(gboard.board['black'])
  #print(gboard.rotate()) # 8===D~~ owo made me sploogie