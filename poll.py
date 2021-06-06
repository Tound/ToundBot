class poll:
    def __int__(self,name,args):
        self.name = name
        self.choices = args
        self.votes = []
        self.totalVotes = 0

    def vote(self, choice):
        if choice.lower() in self.choices:
            index = self.choices.index(choice)
            self.votes[index] += 1
            self.totalVotes += 1

    def results(self):
        string = ""
        for i in range(0,len(self.choices)):
            string += f"{self.choices[i]}: ["
            percentage = int(20*self.votes[i]/self.totalVotes)
            for j in range(0,20):
                if j < percentage:
                    string += "#"
                else:
                    string += " "
            string += "] {} \n"
        string += f"Total votes: {self.totalVotes} \n"
        return string

    def addChoice(self,choice):
        self.choices.append(choice)
        self.vote(choice)

    def getChoices(self):
        return self.choices

    def close(self):
        string = self.results()
        min_votes = 0
        for i in range(0,len(self.votes)):
            if self.votes[i] > min_votes:
                index = i
        string += f"Poll closed! \n {self.choices[index]}"
        return string
