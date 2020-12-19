class gamesnight:
    def __init__(self, title, time, members, games):
        self.title =  title
        self.time = time
        self.members = members
        self.games.append(games)

    def __int__(self, games, members):
        self.title = None
        self.game.append(games)
        self.time = None
        self.members.append(members)

    def __int__(self, games):
        self.title = None
        self.games.append(games)
        self.time = None
        self.members = []

    def addPlayer(self, name):
        self.players.append(name)

    def addGame(self, game):
        self.game.append(game)

    def setTime(self, time):
        self.time = time

    def setTitle(self, title):
        self.title = title

    def getAnnouncement(self):
        if self.time == None:
            return f"Time has not been set for this Game Night"
        elif self.title == None:
            return f"The title has not been set for the Games Night!"
        else:
            return f"<< {self.title} >> \n Will begin at {self.time}"

    def getCountdown(self, currentTime):
        timeTill = self.time - currentTime
        if self.time == None:
            return f"Time has not been set for this tournament"
        elif self.title == None:
            return f"There is {timeTill} till the Games Night!"
        else:
            return f"There is {timeTill} till the {self.title} Games Night!"
