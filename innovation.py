class Innovation:
    currentInnovation = 1

    def getInnovation(self):
        self.currentInnovation = self.currentInnovation + 1
        return self.currentInnovation-1


