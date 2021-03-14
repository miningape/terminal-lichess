# To do list
- [x] Display the chess board we made in chess.py in poop.py
  - [x] Actual grid needs o get expanded to 10x10
  - [x] have custom_print_cell() look at the chessboard we make and then just change the value of that cell accordingly
  - [x] remember we have to have whitespace easiest way is:
  ```python
    "     \n    {}   \n     {}".format( args, args )
  ```
  - [ ] remember the format of the chessSetup board is "charcharchar" first char is square color, next is the kind of piece and the last is the color of that piece, "charNN" denotes that the square has No piece with No color
  - [ ] "DIchar" is used for the characters around the edge of the board(maybe some formatting there would be nice)
  - [ ] Try testing moves/over time, create a Thread.timer for a few seconds, then move a piece and redraw the grid to see if it works
- [ ] Mess with the api, figure out how to make moves and stuff (theres a little stuff in api.py but it only gets current board state)
  - [ ] We need to start (bot) game then start listening to that game
  - [ ] We need to be able to make moves
  - [ ] Maybe ability to switch api keys
  - [ ] anything else on the lichess api docs that looks usefulk
  - [x] Remember to multithread, cus we need a stream open while also sending data and displaying the stuffs
- [ ] Try making an API class so we can get/send moves and interact with poop.py/chess.py

* Menu screen
* Challenge a bot
* Premoves
* Game win/draw/loss etxc and resign
* Show all moves in the game so far
* Color changing
* Show all moves made previously
* Show what piece is what4
* Move the main IO thread to the app class so it can be shared by several forms
* Tell player what color they are?
* 
* Better outputs telling the user what is going on

[x] Castling
* custom game Id

# IDK if chess.py needs any updates but you can look