from twisted.web.resource import Resource
from app.db import db


# Copied from https://twistedmatrix.com/documents/15.0.0/web/howto/using-twistedweb.html
# We don't need to use this, just trying to demonstrate it to joel
class Games(Resource):
    isLeaf = True
    def getChild(self, name, request):
        if name == '':
            return self
        return Resource.getChild(self, name, request)

    def render_GET(self, request):
        return # Query db

# 'http://michaelsdomain.com/games'

root = Games()
root.putChild('games', Games())

# /games
# Returns all of the current games that are running

# /game/<id>/lobby
# Returns current players

# /game/<id>/running
# Return current state of game



