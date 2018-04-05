class NodeGene:
    def __init__(self, id, nodeType):
        self.id = id
        self.nodeType = nodeType

    def copy(self):
        return NodeGene(self.id, self.nodeType)
