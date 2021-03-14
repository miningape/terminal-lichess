# PYTHON PACKAGES
import npyscreen
import threading

# OUR OWN FILES
import template             # npyscreen form classes
import color as theme       # npyscreen theme class
import chess                # Chess board info class
import api                  # Networking api
import helper               # Helper Methods class


# Globals that need to be shared across all forms/threads/widgets
# ! Needs Refactoring: Ideally it would be in App(), this code was written to make it easy
lapi = api.lichessReq()
g_chessState = chess.ChessState()

# ! Should be in template.py, but it relies on g_chessState, so it stays here until further notice
class ChessBoardDisplay(npyscreen.SimpleGrid):
  _contained_widgets = npyscreen.MultiLineEdit
  default_column_number = 8
  def custom_print_cell(self, actual_cell, cell_display_value):
    # IDK WHY BUT THIS UGLYNESS IS REQUIRED OR ELSE IT SHITS THE BED
    # I DONT EVEN WANT TO KNOW WHY RANDOM CELLS WITH GRID INDEX -1 (this is a 2d array) GET PASSED IN
    if (actual_cell.grid_current_value_index) == -1:
      actual_cell.color='CURSOR'

    else:#Behaving sensibly
      g_cur_board = g_chessState.cur_board()
      coords   = actual_cell.grid_current_value_index
      cur_cell = g_cur_board[coords[0]][coords[1]] # Get the cell we are currently in
      cellInfo = helper.splitstr( cur_cell )          # Extract info from that cell
      [cellColor, piece, pieceColor] = cellInfo       # Make the info easy to access

      if (cellColor == 'D' and piece == 'I'):         # In this case we are on the edge of board and need a label
        actual_cell.color = 'CURSOR'
        actual_cell.value =  '       \n   {}   \n       '.format( pieceColor )
      else:
        # Set the piece and cell color
        if not(piece == 'N' and pieceColor == 'N'):
          actual_cell.color = pieceColor
          actual_cell.value = '       \n   {}   \n       '.format( piece )
        else:
          actual_cell.color = 'B'
          actual_cell.value = '       \n       \n       '

        if cellColor == 'B':
          actual_cell.color += '_Y'
        elif cellColor == 'W':
          actual_cell.color += '_C'
        else:
          pass # <-- Change to throw an error

# Main Menu / Landing Menu
class menuForm(template.CustomMenu):
  num_ongoing_games = 0
  # Event stream handler
  def generalJSON(self, json):
    req = json['type']
    
    if req == 'gameStart':
      gameID = json['game']['id']
      #print(gameID)
      self.num_ongoing_games += 1
      #npyscreen.blank_terminal()
      #npyscreen.notify_ok_cancel('It looks like there is a game (ID: {}) that has already started.\n.\n.\n\tDo you want to connect to it?'.format(gameID))
      self.output.value = '\nIt looks like are {} games that have already started.\nTo join open the menu (ctrl+X), and select "Join Ongoing Game"'.format(self.num_ongoing_games)
      self.menu.addItem(gameID, self.switch_and_join, None, arguments=(gameID,)) 
      self.display()
   
  # Functions that output text to the user
  def usage(self):
    npyscreen.notify_confirm('To Use This Client: you will need to start a bot game. After starting the game you should see a large chess board in front of you.\n-----\nTo make a move type the move in the black box in the bottom left. The format for these moves is square from square to, and letter before number. For example to move a piece from the e1 square to e2, you would type "e1e2", without quotation marks.\n-----\nCastling is handled by typing the square the king lands on as the square to (e.g. "e1g1").\n-----\nWe have tried to guess what color the player is and set the board up from their perspective, however this doesn\'t mean that it is always correct, to flip the board, select the menu and then "flip board".\n-----\nTo resign/draw a game, select resign/draw in the menu, confirming a draw is done in the same way offering a draw is.\n-----\nThe pieces are as follows:\nK:\tKing \nQ:\tQueen\nB:\tBishop\nN:\tKnight\nR:\tRook\nP:\tPawn', wide=True, title="Tutorial")
  
  def client(self):
    npyscreen.notify_confirm('This LiChess terminal client was written by Kyle Johnson and Daniel Lyakhobich, for an assignment in \"Interactive Digital Systems\" at Roskilde University.\n-----\nIt interacts with LiChess.org through its api LiChess.org/api, and is written in python, using npyscreen, ncurses, requests and threading', wide=True, title="Client Info")

  def todo(self):
    npyscreen.notify_confirm('1)\tActual Online Multiplayer\n2)\tInputting Your Own API Key\n3)\tRead/Write In Game Chats\n4)\tMake Sure Orientation is Correct\n4)\tPlayer/API information\n5)\tChange colors', wide=True, title="To Do List:")

  def lichess(self):
    npyscreen.notify_confirm('Lila (li[chess in sca]la) is a free (open-source) online chess game server focused on realtime gameplay and ease of use.\n-----\nIt features a search engine, computer analysis distributed with fishnet, tournaments, simuls, forums, teams, tactic trainer, a mobile app, and a shared analysis board.\n-----\nLichess is written in Scala 2.13, and relies on the Play 2.8 framework. scalatags is used for templating. Pure chess logic is contained in the scalachess submodule. The server is fully asynchronous.', wide=True, title="LiChess.org Info")
  
  # semi-constructor that handles the adding of all the elements that can be seen
  def create(self):
      # Adding output text
      self.logo = self.add(npyscreen.MultiLineEdit, editable=False, height=12)
      self.output = self.add(npyscreen.MultiLineEdit, value="", editable=False, height=3)
      self.add(npyscreen.MultiLineEdit, value="", editable=False, height=3)
      self.add(npyscreen.MultiLineEdit, value="This Version (1.0.4) Does Not Support Player to Player games, or custom API keys", editable=False, height=3, color='WARNING')
      
      # Adding menu options
      self.menu = self.add_menu(name="Join Ongoing Game", shortcut="j")
      #self.res_menu = self.add_menu(name="Resign Ongoing Game", shortcut="r")

      self.info_menu = self.add_menu(name="App Info", shortcut="H")
      self.info_menu.addItem('Usage', self.usage, 'u')
      self.info_menu.addItem('Client Info', self.client, 'a')
      self.info_menu.addItem('Planned Features', self.todo, 'p')
      self.info_menu.addItem('LiChess', self.lichess, 'l')

      #self.testing_menu = self.add_menu(name="Testing", shortcut="t")
      #self.testing_menu.addItem('All', None, 'a')
      #self.testing_menu.addItem('Networking', None, 'n')
      #self.testing_menu.addItem('Chessboard', None, 'c')
      
      self.logo.value = " ▄            ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄         ▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ \n"\
                        "▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌\n"\
                        "▐░▌           ▀▀▀▀█░█▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ ▐░█▀▀▀▀▀▀▀▀▀ \n"\
                        "▐░▌               ▐░▌     ▐░▌          ▐░▌       ▐░▌▐░▌          ▐░▌          ▐░▌          \n"\
                        "▐░▌               ▐░▌     ▐░▌          ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ \n"\
                        "▐░▌               ▐░▌     ▐░▌          ▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌\n"\
                        "▐░▌               ▐░▌     ▐░▌          ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀█░▌ ▀▀▀▀▀▀▀▀▀█░▌\n"\
                        "▐░▌               ▐░▌     ▐░▌          ▐░▌       ▐░▌▐░▌                    ▐░▌          ▐░▌\n"\
                        "▐░█▄▄▄▄▄▄▄▄▄  ▄▄▄▄█░█▄▄▄▄ ▐░█▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄█░▌ ▄▄▄▄▄▄▄▄▄█░▌\n"\
                        "▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌\n"\
                        " ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀  ▀▀▀▀▀▀▀▀▀▀▀ "
  # Switch form and join specific game
  def switch_and_join(self, gameID):
    self.parentApp.switchForm('GAME')
    self.parentApp.getForm('GAME').GAMEID = gameID      # Set the game id to the game we want
    self.parentApp.getForm('GAME').START_GAME_THREAD()  # Start the game stream thread on the ID we just set
    self.parentApp.curForm = 'GAME'
  
  # Buttons at the bottom of the screen overrides
  def on_exit(self):
    self.parentApp.setNextForm(None)
  
  def on_play_bot(self):
    self.parentApp.switchForm('SETUP')
    self.parentApp.curForm = 'SETUP'
  
  def on_settings(self):
    print('settings is broken')

 # This is where the actual game logic takes place
class mainForm(template.CustomForm):
  movesMade = ''
  playingGame = False
  GAMEID = None
  GameCompleteFlag = False

  # Button overrides
  def on_ok(self):
    # Close general io threading
    self.CLOSE_GAME_THREAD()
    self.parentApp.switchForm('MAIN')
    self.parentApp.curForm = 'MAIN'
  
  def on_send(self):
    userMove = self._added_buttons['input_box'].value # Text inside user input
    response = lapi.makeMove(userMove, self.GAMEID)
    if 'error' in response.json():
      self.outputText.value = response.json()['error']

  def exit(self):
    self.CLOSE_GAME_THREAD()
    self.parentApp.switchForm(None)

  # Game Thread Helper Functions
  def CLOSE_GAME_THREAD(self):
    if self.playingGame:
      lapi.game_flag = True
      self.game_thread.join()
    #Otherwise thread closes itself
    
  def START_GAME_THREAD(self):
    self.game_thread = threading.Thread(target=lapi.gameState, args=( self.handleJSON, self.firstHandleJSON, self.GAMEID, ))
    self.playingGame = True      
    self.game_thread.start()
  
  def GameOverMSG( self ):
    self.gameInfoText.value = 'Game (ID: {}) Is Over. {} made {} win'.format(self.GAMEID, self.gameMSG, self.gameWinner)
    self.display()
    self.playingGame = False
    self.outputText.value = 'Disconnected'
    # Thread closes itself as the connection closes when the game does

  # Game stream handler (every time but the first)
  def handleJSON(self, json):
    status = json['status']
    if status != 'started':
      self.gameMSG = status
      if self.latestMove != json['moves'][-4:]:
        self.movesMade = json['moves']
        self.move_and_update(self.latestMove)

      if 'winner' in json:
        self.gameWinner = json['winner']
      else:
        self.gameWinner = 'No one'

      if self.GameCompleteFlag:
        self.GameOverMSG()
      else:
        self.GameCompleteFlag = True

    else:
      listOMoves = json['moves']
      self.latestMove = listOMoves.split()[-1]
      self.movesMade = listOMoves
      self.move_and_update(self.latestMove)
  
  # Game stream handler for the initial response from the game stream (this is because this response and all folowing responses have a different JSON structure)
  def firstHandleJSON(self, json):
    self.gameInfoText.value = 'Game (ID: {}) In Play'.format(json['id'])
    self.latestMove = json['state']['moves'].split()[-1] if json['state']['moves'] != "" else "Nothing, Your Move"
    self.many_move(json['state']['moves'])
  
  # Event Stream Handler
  def generalJSON(self, json):
    # Figure out what kind of request we recieved
    req = json['type']

    # Should probably be moved to app, to notify the user, change form and then begin thred
    if req == 'gameStart':    # ex: {"type":"gameStart","game":{"id":"S3cxPmhA"}}
      self.gameInfoText.value = 'Game (ID: {}) In Play'
      self.GAMEID = json['game']['id']
      self.START_GAME_THREAD()

    # Should be changed to show the game is over
    elif req == 'gameFinish': # ex: {"type":"gameFinish","game":{"id":"S3cxPmhA"}}
      self.close_GAMEID = json['game']['id']
      
      if self.close_GAMEID == self.GAMEID:   # Check to make sure that random interference doesnt suddenly close the game
        if self.GameCompleteFlag:
          self.GameOverMSG()
        else:
          self.GameCompleteFlag = True

  # Move a piece on the board, and then tell npyscreen to draw the screen again
  def move_and_update(self, move):
    g_chessState.make_move(move)
    self.outputText.value = 'Last move: {}'.format(move)
    self.display()

  # Make several moves in a row (generally only called at the beginning of the game as the api doesnt garantee the first connection only contains one move)
  def many_move(self, moves):
    self.outputText.value = 'GAME STARTED!\nCurrent moves are {}'.format(moves)
    g_chessState.start(moves)
    self.movesMade = moves
    self.display()
  
  # Helper function to resign
  def resignGame(self):
    lapi.resignGame(self.GAMEID)
   
  # Show all the moves made throughout the game
  def showMoves(self):
    npyscreen.notify_confirm( self.movesMade, title="Moves Made", editw=1 )
  
  # Helper to show that a feature has been disabled
  def showBroken(self):
    npyscreen.notify_confirm( "Sorry Action Unavailable", title="Error", editw=1, form_color="DANGER" )

  # Pseudo constructor that adds elements to the screen
  def create(self):
    # Custom menu keybind not really important we were just messing with it (ctrl-x is preffered over ctrl-g)
    self.add_handlers({'^G': self.root_menu})

    # Actual board display
    self.mygrid = self.add(ChessBoardDisplay, name="Something", columns=10, column_width=7 , row_height=3, col_margin=0, editable=False )

    # Text elements to output to
    self.outputText = self.add(npyscreen.MultiLineEdit, value="keybind: ^X", relx = 80, rely=10, editable=False)
    self.outputText.value = "Not Playing" if not self.playingGame else "Playing, this text shouldnt be here"
    self.gameInfoText = self.add(npyscreen.MultiLineEdit, value="", relx = 80, rely=15, editable=False, color='GOOD')

    #Menus
    self.menu = self.add_menu(name="Menu", shortcut="c")
    #self.m2 = self.add_menu(name="Another Menu", shortcut="b",)
    self.menu.addItem("Flip Board", g_chessState.flip, "f") 
    self.menu.addItem("Show All Moves", self.showMoves, "m") 
    self.menu.addItem("Resign Game", self.resignGame, "r") 
    self.menu.addItem("Offer Draw (Not for AI)", self.showBroken, "d") 
    self.menu.addItem("Exit App", self.exit, None ) 
    
    # Grid creation
    self.mygrid.values = []
  
    for x in range(10):
      cur_row = []
      for y in range(10):
        cur_cell = 'CELL'
        cur_row.append(cur_cell) 
      self.mygrid.values.append(cur_row)

# Form for selecting color/difficulty
class gameSetup(template.NETWORKEDFORM):
  MAP = ['random', 'black', 'white']      # Map between selected value and what the api expects

  # Event stream handler (again) this time it waits for a game to start, once it does it changes the form to the game screen and changes the gameID to the correct on
  # Not the best way to handle the creation of a game as if you create a game, then during the processing of that request another game is started you will be sent to the other game
  def generalJSON( self, json ):
    req = json['type']
    
    if req == 'gameStart' and json['game']['id']:
      self.parentApp.switchForm('GAME')
      self.parentApp.getForm('GAME').GAMEID = json['game']['id']
      self.parentApp.curForm = 'GAME'
      # Very hacky code, should probably make an explicit method to add to ongoing game list, rather than just propegating the call
      self.parentApp.getForm('MAIN').generalJSON(json)
      self.parentApp.getForm('GAME').generalJSON(json)
  
  # Button overrides
  def on_cancel(self):
    self.parentApp.switchForm('MAIN')
    self.parentApp.curForm = 'MAIN'
  
  def on_ok(self):
    self.createText.hidden = False    # Show "creating game..."
    lapi.makAIGame( int(self.difficulty.value), self.MAP[self.choice.value[0]] )    # Create a request on the api to start a game
    g_chessState.setState( self.MAP[ self.choice.value[0] ] )                       # Set the orientation of the board

  # Pseudo contsructor adding elements to the screen
  def create(self):
    self.difficulty = self.add(npyscreen.TitleSlider, out_of=8, step=1, lowest=1, name='Difficulty', value=1)
    self.add(npyscreen.Textfield, editable=False)
    self.choice= self.add(npyscreen.TitleSelectOne, name='Color', values= ['Random', 'Black', 'White'], value=[0], height=4)
    #self.add(npyscreen.Textfield, editable=False)
    self.createText = self.add(npyscreen.Textfield, value="Creating Game...", hidden=True, editable=False, color="GOOD")

# Actual app
class App(npyscreen.NPSAppManaged):
  curForm = 'MAIN'
  
  def JSONhandler(self, json):
    self.getForm( self.curForm ).generalJSON( json )

  def onCleanExit(self):
    lapi.main_flag = True
    self.general_network_thread.join()

  def onStart(self):
    npyscreen.setTheme(theme.colors)
    self.addForm('MAIN', menuForm, name="LiChess Terminal Client")
    self.addForm('GAME', mainForm, name="GAME")
    self.addForm('SETUP', gameSetup, name="Setup Bot Game")

    self.general_network_thread = threading.Thread(target=lapi.generalStream, args=(self.JSONhandler, ))
    self.general_network_thread.start()
    
    

if __name__ == '__main__':
  app = App()
  app.run()
