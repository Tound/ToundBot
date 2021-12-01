class Poll:
    def __init__(self,name,track_voters,args):
        self.status = True
        self.name = name
        self.choices = args
        self.votes = [0,0]
        self.voters = []
        self.track_voters = track_voters
        if len(self.votes) != len(args):
            diff = len(args) - len(self.votes)
            for i in range(0,diff):
                self.votes.append(0)

        self.totalVotes = 0

    def vote(self, user, choice):
        print(self.track_voters)
        if self.track_voters and user in self.voters:
            return 1
        elif user not in self.voters:
            self.voters.append(user)
        else:
            pass

        if choice in self.choices:
            index = self.choices.index(choice)
            self.votes[index] += 1
            self.totalVotes += 1
            return 0

        elif int(choice) > 0 and int(choice) < len(self.choices):
            self.votes[int(choice) + 1] += 1
            self.totalVotes += 1
            return 0

        else:
            return -1

    def results(self):
        string = f"{self.name}\n"
        #longest_string = (len(max(self.choices, key=len)) + 1) * 2
        for i in range(0,len(self.choices)):

            string += "["

            if self.totalVotes == 0:
                percentage = 0
            else:
                percentage = int(50*self.votes[i]/self.totalVotes)
            for j in range(0,50):
                if j < percentage:
                    string += "#"
                else:
                    string += "="
            string += f"] {self.choices[i]}: {self.votes[i]}\n"
        string += f"Total votes: {self.totalVotes} \n"
        return string

    def addChoice(self,choice):
        self.choices.append(choice)
        self.vote(choice)

    def getChoices(self):
        return self.choices

    def open(self):
        self.status = True


    def close(self):
        string = self.results()
        min_votes = 0
        #for i in range(0, len(self.votes)):
        #    if self.votes[i] > min_votes:
        #        index = i
        #string += f"Poll closed! \n {self.choices[index]}\n" \

        indexes = []
        for i in range(0, len(self.choices)):
            if self.votes[i] == max(self.votes):
                indexes.append(i)

        if len(indexes) > 1:
            string += f"Winners: {self.choices[self.votes.index(max(self.votes))]}"
            for i in range(0,len(indexes)):
                string += f"{self.choices[i]}"
        else:
            string += f"Winner: {self.choices[indexes[0]]}"

        return string
