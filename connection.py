class Connection:
    def __init__(self, node1, node2, strength):
        self.node1 = node1
        self.node2 = node2
        self.weight = strength
        self.decay = 100
        self.failed = False
