class tournament:
    def __init__(self, game, players, time):
        self.time = time
        self.games.append(game)
        self.players.append(players)

    def __int__(self, game, players):
        self.games.append(game)
        self.time = 0
        self.players.append(players)

    def __int__(self, game):
        self.games.append(game)
        self.time = 0
        self.players = []

    def addPlayer(self, name):
        self.players.append(name)

    def addGame(self, game):
        self.games.append(game)

    def setTime(self, time):
        self.time = time

    def getTime(self):
        return self.time

    def getGames(self):
        return self.games

    def getPlayers(self):
        return self.players

    def getAnnouncement(self):
        if self.time == None:
            return f"Time has not been set for this Game Night"
        elif self.title == None:
            return f"The title has not been set for the Games Night!"
        elif self.games == None:
            return f"Games to be played has not been set!"
        else:
            return f"<< **{self.title}** >> \n Will begin at {self.time} \n Games being played: {self.games}"
