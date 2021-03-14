import requests   # HTTP REQUEST PACK
import json       # JSON INTERPRETING PACK

class apu():
  game_flag = False
  main_flag = False
  URL = 'https://lichess.org/api'
  
  #GAMEID = 'KLZhrtYV'
  CHALLENGE_AI_URI = '/challenge/ai'
  RESIGN_GAME_URI  = '/board/game/{}/resign'
  EVENT_URI   = '/stream/event'
  STREAM_URI  = '/board/game/stream/'
  MOVE_URI    = '/board/game/{}/move/{}'

  # Our API keys in a dictionary,!!! MAKE SURE TO ENCRYPT !!!
  KEYS = {
    'daniel': 'bDeg8BKxQwF6Z5PI',
    'kyle'  : 'xQfew70rgwOQI9OJ'
  }

  # Required Header is: "Authorization: Bearer <token>"
  REQUEST_HEAD = {'Authorization': ('Bearer ' + KEYS['kyle'])}

  def makAIGame( self, difficulty, color ):
    rURL = self.URL + self.CHALLENGE_AI_URI
    REQUEST_BODY = {'level': difficulty, 'clock.limit': None, 'clock.increment': None, 'days': None, 'color': color, 'variant': 'standard', 'fen': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'}

    request = requests.post( rURL, headers=self.REQUEST_HEAD,json=REQUEST_BODY )

    # Debugging. 
    return request.json()

  def makeMove( self, move, GAMEID ):
    rURL = self.URL + self.MOVE_URI.format( GAMEID, move )
    request = requests.post( rURL, headers=self.REQUEST_HEAD )

    return request
  
  def resignGame( self, GAMEID ):
    rURL = self.URL + self.RESIGN_GAME_URI.format( GAMEID )

    r =requests.post( rURL, headers=self.REQUEST_HEAD )
    return r.json()
  

  def generalStream( self, eventCallback ):
    rURL = self.URL + self.EVENT_URI
    request = requests.get( rURL, headers=self.REQUEST_HEAD, stream=True )

    if request.encoding is None:
      request.encoding = 'UTF-8'
      
    self.main_flag = False
    for data in request.iter_lines(decode_unicode=True):
      if self.main_flag:
        break
      
      if data:
        eventCallback( json.loads(data) )


  def gameState( self, callback, firstCB, GAMEID, waitCB = lambda : None ):
    # Creating request on lichess
    rURL = self.URL + self.STREAM_URI + GAMEID
    request = requests.get(rURL, headers=self.REQUEST_HEAD, stream=True)

    # If the encoding is fucked, fix it
    if request.encoding is None:
      request.encoding = 'UTF-8'
    flag = False

    self.game_flag = False
    # Finally iterate through the data, this continues indefinately
    for data in request.iter_lines(decode_unicode=True):
      if self.game_flag:
        break

      if flag:
        if data:
          callback( json.loads(data) ) # Some observer
        else:
          waitCB()
      else:
        firstCB( json.loads(data) )
        flag = True

      


if __name__ == '__main__':
  api = apu()
  #threading.Thread(target=gameState).start()
  #threading.Timer(5, print, args=(l,)).start()
  #api.gameState( print, print )
  #print( api.makAIGame(8, 'black') )
  print(api.resignGame(''))
   
#{'error': 'Invalid UCI: d5e'}
# { "ok": true }