class Innovation:
    currentInnovation = 0

    def getInnovation(self):
        self.currentInnovation = self.currentInnovation + 1
        return self.currentInnovation-1


