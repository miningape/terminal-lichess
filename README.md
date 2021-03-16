# terminal-lichess
LiChess Terminal Client

# Usage Warning
Because the lichess api only allows one connection to a URI from a single API key, two players cannot play at the same time. If another person starts testing/playing at the same time as you your connection will be dropped from the Lichess API.

# External Dependencies
* npyscreen
* npyscreen is dependent on curses/win-curses (should only need to be installed on windows)
```terminal
pip install npyscreen
pip install windows-curses
```

# Running
```terminal
cd src/
python game.py
```
